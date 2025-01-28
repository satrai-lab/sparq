package composer;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

//import iotSys.broker.App;
//import iotSys.broker.JsonParser;
import iotSystemComponents.Application;
import iotSystemComponents.IoTdevice;
import iotSystemComponents.Subtopic;
import iotSystemComponents.Topic;
import iotSystemComponents.VirtualSensor;
import jmt.gui.common.definitions.CommonModel;
import jmt.gui.common.xml.XMLWriter;

public class QueueingNetworkComposer {

	public static HashMap<String, Subtopic> subtopics = new HashMap<String, Subtopic>();
	public static Object FCR_OBJECT;

	public String composeNetwork(String inputFile, int strategyId, List<String> arguments)
			throws Exception {
		
		inputFile = checkFileName(inputFile, strategyId);
		JsonParser parser = new JsonParser();
		parser.readJSON(inputFile);

		String priorityPolicy = JsonParser.priorityPolicy;

		CommonModel jmtModel = new CommonModel();
		IoTdeviceHandler iotDeviceHandler = new IoTdeviceHandler();
		HashMap<String, IoTdevice> iotDevices = parser.iotDevices;
		iotDeviceHandler.addSources(jmtModel, iotDevices.keySet());


		ApplicationHandler applicationHandler = new ApplicationHandler();
		HashMap<String, Application> applications = parser.applications;
		applicationHandler.addApplications(jmtModel, applications.values());

		VirtualSensorHandler virtualSensorHandler = new VirtualSensorHandler();
		HashMap<String, VirtualSensor> virtualSensors = parser.virtualSensors;
		virtualSensorHandler.addVirtualSensor(jmtModel, virtualSensors.values());

		TopicHandler topicHandler = new TopicHandler();
		HashMap<String, Topic> topics = parser.topics;
		topicHandler.addTopicsForks(jmtModel, topics);
		topicHandler.addTopicsJoin(jmtModel);
		topicHandler.addTopicsSink(jmtModel);
		topicHandler.addTopicsClassSwitches(jmtModel, topics.keySet());

		ClassHandler classHandler = new ClassHandler();
		classHandler.addClassesForIoTdevices(jmtModel, iotDevices.values(), parser.GLOBAL_MESSAGE_SIZE);
		classHandler.addClassesForVirtualSensors(jmtModel, virtualSensors.values(), parser.GLOBAL_MESSAGE_SIZE);
		classHandler.addClassesForTopics(jmtModel, topics.values());

		DroppingHandler droppingHandler = new DroppingHandler();
		droppingHandler.addDroppingSink(jmtModel);

		topicHandler.addSubTopics(jmtModel, topics.values(), applications, virtualSensors, priorityPolicy);

		HashMap<String, Subtopic> subtopics = topicHandler.subtopics;
//		this.subtopics = subtopics;
		PriorityHandler priorityHandler = new PriorityHandler();
		priorityHandler.convertToJmtPriorities(jmtModel, applications, virtualSensors, subtopics);
		priorityHandler.convertTopicPrioritiesToJmtPriorities(jmtModel, topics, subtopics);
		
		priorityHandler.assignPriorities(jmtModel, subtopics, applications);
		
		classHandler.addClassesForSubtopics(jmtModel, subtopics);

		topicHandler.setClassSwitchMatrix(jmtModel, topics);
		topicHandler.setClassSwitchMatrixForSubtopics(jmtModel, subtopics);
		topicHandler.setTopicsClassSwitchMatrix(jmtModel, subtopics);
		topicHandler.setTopicsClassSwitchDroppingMatrix(jmtModel, subtopics);
		
		BrokerHandler brokerHandler = new BrokerHandler();
		brokerHandler.addInputQueue(jmtModel, "input");
		brokerHandler.addOutputQueue(jmtModel, "outputQueue");

		NetworkResourcesManager networkManager = new NetworkResourcesManager(parser.systemBandwidth,
				parser.bandwidthPolicy, parser.GLOBAL_MESSAGE_SIZE);
		networkManager.allocateResources(subtopics, iotDevices, applications);

		LinkHandler linkHandler = new LinkHandler();
		linkHandler.setConnections(jmtModel, parser, topicHandler.subtopicsClassSwitches);

		FiniteCapacityRegionHandler fcrHandler = new FiniteCapacityRegionHandler();
		Object fcrObj = fcrHandler.setFiniteCapacityRegion(jmtModel, parser.BROKER_CAPACITY, subtopics);
		FCR_OBJECT = fcrObj;

		ServiceTimeHandler serviceTimeHandler = new ServiceTimeHandler();
		serviceTimeHandler.setInputQueueServiceTime(jmtModel, parser.brokers.get(0), topics);
		serviceTimeHandler.setOutputQueueServiceTime(jmtModel, networkManager, subtopics);
		serviceTimeHandler.setApplicationsServiceTime(jmtModel, applications);
		serviceTimeHandler.setVirtualSensorsServiceTime(jmtModel, virtualSensors);
		
		RoutingHandler routingHandler = new RoutingHandler();
		routingHandler.setTopicsClassSwitchRouting(jmtModel, subtopics);
		routingHandler.setApplicationsRouting(jmtModel, applications);
		routingHandler.setInputQueueRouting(jmtModel, topics);
		routingHandler.setOutputQueueRouting(jmtModel, subtopics);
		routingHandler.setVirtualSensorsRouting(jmtModel, virtualSensors);
		routingHandler.addDroppingRouting(jmtModel, subtopics, topicHandler.subtopicsClassSwitches,
				parser.CHANNEL_LOSS_AN, parser.CHANNEL_LOSS_RT, parser.CHANNEL_LOSS_TS, parser.CHANNEL_LOSS_VS);

		PerformanceMetricsHandler performanceMetricsHandler = new PerformanceMetricsHandler();
		double confInterval = 0.95;
		double relErr = 0.05;
		performanceMetricsHandler.setPerformanceMetrics(jmtModel, subtopics, fcrObj, confInterval, relErr);

		
		//applying mitigation strategy
		inputFile = applyMitigationStrategy(jmtModel, inputFile, strategyId, arguments);
		
//		int dirIndex = inputFile.lastIndexOf(System.getProperty("file.separator"));
		int dirIndex = inputFile.lastIndexOf('/');
		int i = inputFile.lastIndexOf(".");
		// save jmt files in a 'jsimg' directory

		Path filePath = Paths.get(inputFile.substring(0, dirIndex), "jsimg",
				inputFile.substring(dirIndex, i) + ".jsimg");
//		 String jsimgFilePath =  inputFile.substring(0, dirIndex) + "/jsimg/" + inputFile.substring(dirIndex, i) + ".jsimg";
		File jsimFile = new File(filePath.toString());
		XMLWriter.writeXML(jsimFile, jmtModel);

		return filePath.toString();

	}
	
	
	public static String applyMitigationStrategy(CommonModel jmtModel, String inputFile, int strategyId, List<String> arguments) {
		if (strategyId == 18 || strategyId == 19) {
			inputValidation(jmtModel, arguments); // input validation / packet dropping /
		} else if (strategyId == 20 || strategyId == 21 || strategyId == 24) {
			networkDisconnection(jmtModel, arguments); // network disconnection / process termination / switch off device
		} else if (strategyId == 1) {		
			updateSoftware(jmtModel, arguments);		//update software
		}
		//the following strategies are handled by the python script -- nothing needs to be done here.
		//We only change the name of the input file to match the newly created file
		else if (strategyId == 2 || strategyId == 9 || strategyId == 22) {
			inputFile = inputFile.replace("-default", "");
		}
		return inputFile;
	}
	
	public static String checkFileName(String inputFile, int strategyId) {
		if (strategyId == 2 || strategyId == 9 || strategyId == 22 || strategyId == 10 || strategyId == 11 || strategyId == 13) {
			return inputFile.replace("-default", "");
		}
		return inputFile;
	}

	public static void inputValidation(CommonModel jmtModel, List<String> arguments) {
		LinkHandler linkHandler = new LinkHandler();
		ClassHandler classHandler = new ClassHandler();
		for (String app : arguments) {
			linkHandler.removeAppConnection(jmtModel, app);
			classHandler.removeClassForSubtopics(jmtModel, subtopics, app);
		}
	}

	public static void networkDisconnection(CommonModel jmtModel, List<String> arguments) {
		LinkHandler linkHandler = new LinkHandler();
		ClassHandler classHandler = new ClassHandler();
		TopicHandler topicHandler = new TopicHandler();
		IoTdeviceHandler deviceHandler = new IoTdeviceHandler();
		for (String device : arguments) {
			linkHandler.removeDeviceConnection(jmtModel, device);
			classHandler.removeDeviceClass(jmtModel, device);
			String topicSwitch = "topic_" + device.replace("_source", "");
			topicHandler.removeClassSwitch(jmtModel, topicSwitch);
			deviceHandler.removeDevice(jmtModel, device);
		}
	}
	
	public static void updateSoftware(CommonModel jmtModel, List<String> arguments) {
		ServiceTimeHandler serviceTimeHandler = new ServiceTimeHandler();
		String device = arguments.get(0);
		int delay = Integer.parseInt(arguments.get(1));
		serviceTimeHandler.setDelayServiceTime(jmtModel, device, delay);
	}

	
	/*
	 * Old function -- was trying to add a delay station/queue. Not used anymore
	 */
//	public static void updateSoftware(CommonModel jmtModel, List<String> arguments) {
//		FiniteCapacityRegionHandler fcrHandler = new FiniteCapacityRegionHandler();
//		LinkHandler linkHandler = new LinkHandler();
//		IoTdeviceHandler deviceHandler = new IoTdeviceHandler();
//		ServiceTimeHandler serviceTimeHandler = new ServiceTimeHandler();
//		RoutingHandler routingHandler = new RoutingHandler();
//		String device = arguments.get(0);
//		int delay = Integer.parseInt(arguments.get(1));
//		deviceHandler.addDelayStation(jmtModel, device);
//		linkHandler.connectDelay(jmtModel, device);
//		serviceTimeHandler.setDelayServiceTime(jmtModel, device, delay);
//		routingHandler.addDelayRouting(jmtModel, device);
//		fcrHandler.addDelay(jmtModel, FCR_OBJECT, device);
//	}
}
