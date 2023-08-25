# condor scripts for CLD full sim and reconstruction

here is an example of HNL (long lived particle) production for CLD full simulation and reconstruction

one needs first to generated HNL events.
HNL hepmc : produced with madgraph, electrons channels following same production as the FCC HNL analysis 
(*https://github.com/FCC-LLP/FCCAnalyses/blob/master/examples/FCCee/bsm/LLPs/DisplacedHNL/HNL_sample_creation/mg5_proc_card_HNL_Majorana_eenu_50GeV_1e-5Ve.dat)*
generations is made with madgraph (*https://launchpad.net/mg5amcnlo*) follow the madgraph instructions for installation.

The HNL model can be found at the 
*https://feynrules.irmp.ucl.ac.be/raw-attachment/wiki/HeavyN/SM_HeavyN_CKM_AllMasses_LO.tgz*
the tgz file has to be unziped within the "model" directory of madgraph. 

Generations can be simply be done with 

`bin/mg5_aMC mg5_proc_card_HNL_Majorana_eenu_50GeV_1e-5Ve.dat`

the generation done, the hepmc file is produced in the "events" directory. It has to be unzipped in a dedicated directory "/location/of/hepmcfiles/SampleName"

For the fullsim, one needs for to get CLICPerformance repo
`git clone https://github.com/iLCSoft/CLICPerformance.git`

then the produciton can simply be launch from the script 
`python ProdSim4Physics.py -Nevts_tot="50000" -Nevts_per_job="1000" -Sample="SampleName" -output_sclio="/output/directory/sclio/" -inputFiles="/location/of/hepmcfiles/SampleName"`

Nevts_tot is the total number of events
Nevts_per_job is the number of events per job
the number of jobs is determined from Nevts_tot and Nevts_per_job
Sample is the sample name, not that it should match the last part of the inputFiles path.

Once the fullsim is produced (in the sclio format), the reconstruction is done with the script 
`python ProdReco4Physics.py -Nevts_tot="50000" -Nevts_per_job="1000" -Sample="SampleName" -output_edm4hep="/output/directory/edm4hep/" -inputFiles="/output/directory/sclio/"`

notes that Nevts_tot, Nevts_per_job and Sample should be the same as for the Full sim production
