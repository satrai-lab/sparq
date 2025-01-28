package composer;

import java.util.HashMap;
import java.util.Map;

import iotSystemComponents.Application;
import iotSystemComponents.Subtopic;
import iotSystemComponents.Topic;
import iotSystemComponents.VirtualSensor;
import jmt.gui.common.definitions.CommonModel;
import jmt.gui.common.routingStrategies.ProbabilityRouting;

public class RoutingHandler {

	public void setTopicsClassSwitchRouting(CommonModel jmtModel, HashMap<String, Subtopic> subtopics) {
		Object classSwitch = jmtModel.getStationByName("topics_class_switch");
		for (Subtopic subtopic : subtopics.values()) {
			ProbabilityRouting probaRouting = new ProbabilityRouting();
			probaRouting.getValues().put(jmtModel.getStationByName(subtopic.parentTopicName + "_join"), 1d);
			jmtModel.setRoutingStrategy(classSwitch, jmtModel.getClassByName(subtopic.name + "_class"), probaRouting);
		}
	}

	public void setApplicationsRouting(CommonModel jmtModel, HashMap<String, Application> applications) {
		for (Application app : applications.values()) {
			for (String topicName : app.subscribedTopics) {
				ProbabilityRouting probaRouting = new ProbabilityRouting();
				probaRouting.getValues().put(jmtModel.getStationByName(topicName + "_join"), 1d);
				jmtModel.setRoutingStrategy(jmtModel.getStationByName(app.applicationName),
						jmtModel.getClassByName(topicName + "_class"), probaRouting);
			}
		}
	}

    public void setInputQueueRouting(CommonModel jmtModel, HashMap<String, Topic> topics) {
    	Object inputQueue = jmtModel.getStationByName("input");
    	for (Topic topic : topics.values()) {
    		ProbabilityRouting probaRouting = new ProbabilityRouting();
    		probaRouting.getValues().put(jmtModel.getStationByName(topic.topicName + "_fork"), 1d);
    		jmtModel.setRoutingStrategy(inputQueue, jmtModel.getClassByName(topic.topicName + "_class"), probaRouting);
    	}
    }

//	public void setInputQueueRouting(CommonModel jmtModel, HashMap<String, Topic> topics) {
//		Object inputQueue = jmtModel.getStationByName("input");
//			ProbabilityRouting probaRouting = new ProbabilityRouting();
////			jmtModel.setRoutingStrategy(inputQueue, jmtModel.getClassByName("topic_topic1_class"), probaRouting);
////			probaRouting.addStation(jmtModel.getStationByName("topic_topic1_fork"));
//			System.out.println("Before setting: " + jmtModel.getRoutingStrategy(inputQueue, jmtModel.getClassByName("topic_topic1_class")));
//			
//			probaRouting.getValues().put(jmtModel.getStationByName("topic_topic1_fork"), 0.5d);
//			probaRouting.getValues().put(jmtModel.getStationByName("topic_topic2_fork"), 0.3d);
//			probaRouting.getValues().put(jmtModel.getStationByName("topic_topic3_fork"), 0.2d);
//			System.out.println("Routing Values: " + probaRouting.getValues());
//		
//			jmtModel.setRoutingStrategy(inputQueue, jmtModel.getClassByName("topic_topic1_class"), probaRouting.clone());
//			
//			System.out.println("After setting: " + jmtModel.getRoutingStrategy(inputQueue, jmtModel.getClassByName("topic_topic1_class")));
//	}

	public void setOutputQueueRouting(CommonModel jmtModel, HashMap<String, Subtopic> subtopics) {
		Object outputQueue = jmtModel.getStationByName("outputQueue");
		for (Subtopic subtopic : subtopics.values()) {
			ProbabilityRouting probaRouting = new ProbabilityRouting();
			probaRouting.getValues().put(jmtModel.getStationByName(subtopic.appName), 1d);
			jmtModel.setRoutingStrategy(outputQueue, jmtModel.getClassByName(subtopic.name + "_class"), probaRouting);
		}
	}

	public void setVirtualSensorsRouting(CommonModel jmtModel, HashMap<String, VirtualSensor> virtualSensors) {
		for (VirtualSensor sensor : virtualSensors.values()) {
			for (String topicName : sensor.subscribedTopics) {
				ProbabilityRouting probaRouting = new ProbabilityRouting();
				probaRouting.getValues().put(jmtModel.getStationByName(topicName + "_join"), 1d);
				jmtModel.setRoutingStrategy(jmtModel.getStationByName(sensor.deviceName + "_processing"),
						jmtModel.getClassByName(topicName + "_class"), probaRouting);
			}
		}
	}

	// rewrite to support multiple application categories
	public void addDroppingRouting(CommonModel jmtModel, HashMap<String, Subtopic> subtopics,
			HashMap<String, String> subtopicsClassSwitches, double droppingAN, double droppingRT, double droppingTS,
			double droppingVS) {
		for (String subtopicName : subtopicsClassSwitches.keySet()) {
			String className = subtopicName + "_class";
			String classSwitchName = subtopicsClassSwitches.get(subtopicName);
			ProbabilityRouting probaRouting = new ProbabilityRouting();
			double channelLoss = 0;
			if (subtopics.get(subtopicName).category.equals("AN"))
				channelLoss = droppingAN;
			else if (subtopics.get(subtopicName).category.equals("RT"))
				channelLoss = droppingRT;
			else if (subtopics.get(subtopicName).category.equals("TS"))
				channelLoss = droppingTS;
			else if (subtopics.get(subtopicName).category.equals("VS"))
				channelLoss = droppingVS;
			probaRouting.getValues().put(jmtModel.getStationByName("topics_class_switch_dropping"), channelLoss);
			probaRouting.getValues().put(jmtModel.getStationByName("outputQueue"), 1 - channelLoss);
			jmtModel.setRoutingStrategy(jmtModel.getStationByName(classSwitchName), jmtModel.getClassByName(className),
					probaRouting);
		}
	}

	public void addDelayRouting(CommonModel jmtModel, String device) {
		Object inputQueue = jmtModel.getStationByName("input");
		ProbabilityRouting probaRouting = new ProbabilityRouting();
		probaRouting.getValues().put(jmtModel.getStationByName("topic_" + device.replace("_source", "") + "_fork"), 0d);
		probaRouting.getValues().put(jmtModel.getStationByName(device + "_delay"), 1d);
		jmtModel.setRoutingStrategy(inputQueue, jmtModel.getClassByName(device + "_class"), probaRouting);

	}
}
