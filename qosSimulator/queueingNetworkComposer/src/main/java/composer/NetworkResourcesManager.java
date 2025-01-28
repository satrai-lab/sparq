package composer;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

import org.apache.commons.lang.StringUtils;

import iotSystemComponents.Application;
import iotSystemComponents.IoTdevice;
import iotSystemComponents.Subtopic;

public class NetworkResourcesManager {

	public String allocationPolicy;
	public double totalResources;
	public double allocatedBw_AN;
	public double allocatedBw_RT;
	public double allocatedBw_TS;
	public double allocatedBw_VS;
	
	public double globalMessageSize;
	public static final double GLOBAL_MESSAGE_SIZE = 52428800.0;		//50 MB
	
	public NetworkResourcesManager(double totalResources, String allocationPolicy, double globalMessageSize) {
		this.totalResources = totalResources;
		this.allocationPolicy = allocationPolicy;
		this.globalMessageSize = globalMessageSize;
	}
	
	public void allocateResources(HashMap<String, Subtopic> subtopics, HashMap<String, IoTdevice> devices, HashMap<String, Application> applications) {
		if (allocationPolicy.equals("none")) {
			allocatedBw_AN = totalResources;
			allocatedBw_RT = totalResources;
			allocatedBw_TS = totalResources;
			allocatedBw_VS = totalResources;
		}
		
		else if (allocationPolicy.equals("shared")) {
			allocatedBw_AN = totalResources / 4;
			allocatedBw_RT = totalResources / 4;
			allocatedBw_TS = totalResources / 4;
			allocatedBw_VS = totalResources / 4;
		}
		
		else if (allocationPolicy.equals("maxmin")){
			HashMap<String, Double> loadPerCategory = new HashMap<String, Double>();
			loadPerCategory.put("AN", 0d);
			loadPerCategory.put("RT", 0d);
			loadPerCategory.put("TS", 0d);
			loadPerCategory.put("VS", 0d);
			for (Subtopic subtopic : subtopics.values()) {
				String subtopicName = subtopic.name;
				String source = StringUtils.substringBetween(subtopicName, "topic_", "_app") + "_source";
				String app = "app_" + StringUtils.substringBetween(subtopicName, "_app_", "_");
				String category = applications.get(app).applicationCategory;
				IoTdevice device = devices.get(source);
				Double load = device.messageSize * device.publishFrequency;
				Double categoryLoad = loadPerCategory.get(category);
				categoryLoad += load;
				loadPerCategory.put(category, categoryLoad);
			}
			
			ArrayList<Flow> flows = new ArrayList<Flow>();
    		Flow flow_AN = new Flow("AN", loadPerCategory.get("AN"));
    		Flow flow_RT = new Flow("RT", loadPerCategory.get("RT"));
    		Flow flow_TS = new Flow("TS", loadPerCategory.get("TS"));
    		Flow flow_VS = new Flow("VS", loadPerCategory.get("VS"));
    		flows.add(flow_AN);
    		flows.add(flow_RT);
    		flows.add(flow_TS);
    		flows.add(flow_VS);
			ArrayList<Flow> allocatedFlows = maxMinAlgorithm(totalResources, flows);
			
			for (Flow flow : allocatedFlows) {
				if (flow.type.equals("AN")) {
					allocatedBw_AN = flow.allocatedBandwidth;
				}
				else if (flow.type.equals("RT")) {
					allocatedBw_RT = flow.allocatedBandwidth;
				}
				else if (flow.type.equals("TS")) {
					allocatedBw_TS = flow.allocatedBandwidth;
				}
				else if (flow.type.equals("VS")) {
					allocatedBw_VS = flow.allocatedBandwidth;
				}
			}
			
			allocatedBw_AN = allocatedBw_AN/GLOBAL_MESSAGE_SIZE;
			allocatedBw_RT = allocatedBw_RT/GLOBAL_MESSAGE_SIZE;
			allocatedBw_TS = allocatedBw_TS/GLOBAL_MESSAGE_SIZE;
			allocatedBw_VS = allocatedBw_VS/GLOBAL_MESSAGE_SIZE;
		}

	}
    
    public ArrayList<Flow> maxMinAlgorithm(double totalBandwidth, ArrayList<Flow> flows){
		double overflowBandwidth = 0d;
		double sum = 0;
		for (Flow flow : flows) {
			flow.allocatedBandwidth = (totalBandwidth/flows.size()) * GLOBAL_MESSAGE_SIZE;
			sum += flow.requiredBandwidth;
		}
		
		
			
		
		for (Flow flow : flows) {
			if (flow.allocatedBandwidth >= flow.requiredBandwidth) {
				flow.isSatisfied = true;
				overflowBandwidth += (flow.allocatedBandwidth - flow.requiredBandwidth) ;
				flow.allocatedBandwidth = flow.requiredBandwidth;
			}
		}
		
	
		while (overflowBandwidth != 0) {
//			System.out.println("overflow: " + overflowBandwidth / GLOBAL_MESSAGE_SIZE);
			boolean existsFlowUnsatisfied = false;
			int unsatisfiedFlows = 0;
			//check if there are flows that are unsatisfied
			for (Flow flow : flows) 
				if (!flow.isSatisfied) {
					unsatisfiedFlows++;
					existsFlowUnsatisfied = true;
				}
			
			if (!existsFlowUnsatisfied) {
				for (Flow flow : flows) {
//					System.out.println(flow.type  + " before allocation:"  + flow.allocatedBandwidth / GLOBAL_MESSAGE_SIZE);
					flow.allocatedBandwidth += overflowBandwidth / flows.size();
//					System.out.println("after allocation: " + flow.allocatedBandwidth / GLOBAL_MESSAGE_SIZE);
				}
				break;
			}
					
			for (Flow flow : flows) {
				if (!flow.isSatisfied) {
					flow.allocatedBandwidth += overflowBandwidth/unsatisfiedFlows;
				}
			}
			overflowBandwidth = 0;
			
			for (Flow flow : flows) {
				if (flow.allocatedBandwidth >= flow.requiredBandwidth) {
					flow.isSatisfied = true;
					overflowBandwidth += (flow.allocatedBandwidth - flow.requiredBandwidth);
					flow.allocatedBandwidth = flow.requiredBandwidth;
				}
			}

		}
		
		double totalbw = 0;
		for (Flow flow : flows) {
			totalbw += flow.allocatedBandwidth;
		}
		return flows;
	}
}
