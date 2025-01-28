package composer;

import jmt.gui.common.CommonConstants;
import jmt.gui.common.definitions.CommonModel;

public class BrokerHandler {

    public void addInputQueue(CommonModel jmtModel, String inputQueueName) {
		jmtModel.addStation(inputQueueName, CommonConstants.STATION_TYPE_SERVER);
    }
    
    public void addOutputQueue(CommonModel jmtModel, String outputQueueName) {
    	jmtModel.addStation(outputQueueName, CommonConstants.STATION_TYPE_SERVER);
    	jmtModel.setStationQueueStrategy(jmtModel.getStationByName(outputQueueName), CommonConstants.STATION_QUEUE_STRATEGY_NON_PREEMPTIVE_PRIORITY);
    }
    
    public void setOutputQueuePriority(CommonModel jmtModel) {
    	System.out.println(jmtModel.getStationQueueStrategy(jmtModel.getStationByName("outputQueue")));
    	jmtModel.setStationQueueStrategy(jmtModel.getStationByName("outputQueue"), CommonConstants.STATION_QUEUE_STRATEGY_NON_PREEMPTIVE_PRIORITY);
    	System.out.println(jmtModel.getStationQueueStrategy(jmtModel.getStationByName("outputQueue")));
    }
}
