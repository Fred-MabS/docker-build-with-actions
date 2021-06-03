#include <iostream>
#include <omp.h>
#include <sys/stat.h>
#include <sys/types.h>
#include "hex.h"
#include "params.h"
#include "process.h"

using namespace std;

void createDir(const string path)
{
	if (mkdir(path.c_str(), 0755)!=0 && errno!=EEXIST)
		throw runtime_error("(createDir) Could not create '" + path + "' directory.");
}

int main(const int argc, const char* argv[])
{
	if (argc!=2)
	{
		cout << "Requires a configuration file as parameter." << endl;
		return 0;
	}

	const ConfigData config(argv[1]);
	omp_set_num_threads(config.threadCount);

	Params::setupSolvent(config.modelsFolder + "solvent.coor");

	for (vector<DockConfig>::const_iterator dcit=config.dockConfigs.begin(); dcit!=config.dockConfigs.end(); ++dcit)
	{
		const string paramsDirectory = dcit->workDirectory + "params/";
		const string interactionsDirectory = dcit->workDirectory + "interactions/";

		// Creating result directories.
		createDir(paramsDirectory);
		createDir(interactionsDirectory);
		for (vector<PostConfig>::const_iterator pcit=config.postConfigs.begin(); pcit!=config.postConfigs.end(); ++pcit)
		{
			createDir(pcit->formatWorkDirectory(dcit->workDirectory));
			createDir(pcit->formatTopDirectory(dcit->workDirectory));
		}

		// Setting up paths.
		const string hexDirectory = dcit->workDirectory + "hex/";
		Hex hex(config.hexPath, hexDirectory);

		// Calling 'hex'.
		vector<BarePdb> hexModels;
		if (!dcit->bypassHex)
		{
			hex.writeMac(*dcit);

			if (config.benchmarkDirectoryPointer != nullptr)
			{
				const string benchHexDirectory = (*config.benchmarkDirectoryPointer) + "/" + dcit->name + "/hex/";
				const string command = "cp " + benchHexDirectory + "log " + benchHexDirectory + "models.pdb " + hexDirectory;
				if (system(command.c_str()) == -1)
					throw runtime_error("(main) Wrong bench path.");
			}
			else
				hex.run(config.threadCount);

			hex.selectModels(config.maxClashCount);
			hexModels = hex.extractModels();
		}
		else
			cout << "(main) Bypassing hex for config '" << dcit->name << "'. Using '.pdb' files found in '" << dcit->workDirectory << "'." << endl;

		Process process(dcit->workDirectory, hexModels);
		process.computeInteractions(dcit->native, interactionsDirectory,
				config.docksFolder + "type_counts.csv", dcit->name);

		process.gravitateMolecules();
		process.computeParams(*dcit, paramsDirectory);

		process.computeScorings(config.postConfigs);
		process.scoreRegions(config, dcit->epitopeMapping, hex.getLigandPath(), hex.getReceptorPath());
	}

	return 0;
}

