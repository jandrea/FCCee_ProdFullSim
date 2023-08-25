# condor scripts for CLD full sim and reconstruction

here is an example of HNL (long lived particle) production for CLD full simulation and reconstruction. One needs first to generated HNL events in the hepmc format (so including hadronisation).
HNL hepmc files can be produced with madgraph, following same production as for the FCC HNL analysis in arXiv:2203.05502v4. The madgraph parameters can be found at : 
 
 `[MG Card](https://github.com/FCC-LLP/FCCAnalyses/blob/master/examples/FCCee/bsm/LLPs/DisplacedHNL/HNL_sample_creation/mg5_proc_card_HNL_Majorana_eenu_50GeV_1e-5Ve.dat)`

The generations being done with madgraph, one needs to install madgraph

`[MG5](https://launchpad.net/mg5amcnlo) 

Following the madgraph instructions for installation.

The madgraph HNL model can be found at the link :

[HNL MG5 model](https://feynrules.irmp.ucl.ac.be/raw-attachment/wiki/HeavyN/SM_HeavyN_CKM_AllMasses_LO.tgz)

The tgz file has to be unziped within the "model" directory of madgraph.  Generations can be simply be done with the following command :

`bin/mg5_aMC mg5_proc_card_HNL_Majorana_eenu_50GeV_1e-5Ve.dat`

Once the generation is done, the hepmc file is produced in the "events" directory of the process directory. It has to be unzipped in a dedicated directory for further use `/location/of/hepmcfiles/SampleName`. The hepmc file has to be reached by condor, so it has to be either on AFS or EOS.

Then, move to where (on lxplus) you want to run the scripts and get the CLICPerformance repo :

`git clone https://github.com/iLCSoft/CLICPerformance.git`

then the produciton can simply be launch from the script 

`python ProdSim4Physics.py -Nevts_tot="50000" -Nevts_per_job="1000" -Sample="SampleName" -output_sclio="/output/directory/sclio/" -inputFiles="/location/of/hepmcfiles/SampleName"`

`Nevts_tot` is the total number of events, `Nevts_per_job` is the number of events per job. The number of jobs is determined automatically from `Nevts_tot` and `Nevts_per_job`.
`Sample` is the sample name, note that it should match the last part of the inputFiles path.

Once the fullsim is produced (in the sclio format), the reconstruction is done with the script :

`python ProdReco4Physics.py -Nevts_tot="50000" -Nevts_per_job="1000" -Sample="SampleName" -output_edm4hep="/output/directory/edm4hep/" -inputFiles="/output/directory/sclio/"`

notes that `Nevts_tot`, `Nevts_per_job` and `Sample` should be the same as for the Full sim production
