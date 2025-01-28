package composer;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletionService;

import analysis.SimulationResultsWriter;
import jmt.engine.simDispatcher.DispatcherJSIMschema;

public class Main {

	/* args: [0]: json specifications (input file)
	   		 [1]: dataset path (output file)
	   		 [2]: simulation duration (in sec)
	   		 [3]: alias 
	   		 [4]: strategy Id
	   		 [5-...]: remaining args
	*/
	public static void main(String[] args) throws Exception {
		String inputFile = args[0];
		String outputFile = args[1];
		int simulationDuration = Integer.valueOf(args[2]);
		String alias = args[3];
		int strategyId = 0;
		ArrayList<String> arguments = new ArrayList<String>();
		//TODO add checks for arguments
		
		if (args.length > 4) {
			strategyId = Integer.valueOf(args[4]);
			for (int i = 5; i < args.length; i++) {
				arguments.add(args[i]);
			}
		}
		
		QueueingNetworkComposer composer = new QueueingNetworkComposer();
		
		System.out.println("Composing the queueing network ...");
		String jsimgFile = composer.composeNetwork(inputFile, strategyId, arguments);
		System.out.println("Created simulation file.");
		System.out.println("Running the simulation ...");
		DispatcherJSIMschema djss = new DispatcherJSIMschema(jsimgFile);
		djss.setSimulationMaxDuration(simulationDuration*1000);
		djss.solveModel();
		File simResultFile = djss.getOutputFile();
		System.out.println("Simulation done.");
		
		System.out.println("Writing results to csv ...");
		SimulationResultsWriter writer = new SimulationResultsWriter();
		writer.readXML(simResultFile.getCanonicalPath());
		String metricsFile = inputFile.split(".json")[0] + "_" + alias + ".csv";
		writer.writeToCsv(metricsFile);
		System.out.println("Done writing to csv.");
		
		System.out.println("Adding results to dataset");
		writer.addResultsToDataset(outputFile, alias);
		System.out.println("Done.");
		
	}

}
