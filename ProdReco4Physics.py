import os
import argparse
import subprocess
import time;
ts = time.time()


parser = argparse.ArgumentParser(description="Script for running CLD fullsim on Condor")
parser.add_argument("-Nevts_tot", help="Number of events in the hepmc file", required=True)
parser.add_argument("-Nevts_per_job", help="Number of events per condor job", required=True)
parser.add_argument("-Sample", help="Name of the sample", required=True)
parser.add_argument("-output_edm4hep", help="Output file path", required=True)
parser.add_argument("-inputFiles", help="input file path ", required=True)


args = parser.parse_args()

#Nevts_per_job = "1000"
#Nevts_tot     = "50000"
DetectorModelList_ = [ "FCCee_o2_v02"]
#Sample = "HNL_50"
#output_root = "/eos/home-j/jandrea/SampleFCCee_HNL/"
os.system("mkdir "+args.output_edm4hep+"_"+args.Sample+"_RECO_EDM4Hep/")
#inputFiles_ = "/eos/home-j/jandrea/SampleFCCee_HNL/"
#setup = "/cvmfs/sw.hsf.org/key4hep/setup.sh"
setup = "/cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh"

N_jobs = int( int(args.Nevts_tot)/int(args.Nevts_per_job)) +1

print( N_jobs)

directory_sample = "ProdJobs_"+args.Sample+"_RECO_EDM4Hep"
os.system("mkdir "+directory_sample)
   

skip_events = 0
for ijob in range(N_jobs-1):

   directory_job = directory_sample+"/Jobs_"+str(ijob)
   os.system("mkdir "+directory_job)
   print("creating job "+str(ijob)+ " in directory " +directory_job)
   bash_file = directory_job + "/bash_script.sh"
   with open(bash_file, "w") as file:
      file.write("#!/bin/bash \n")
      file.write("source " + setup + "\n")
      file.write("git clone https://github.com/iLCSoft/CLICPerformance.git"+"\n")
      file.write("cd CLICPerformance/fcceeConfig/"+"\n")
      file.write("cp /afs/cern.ch/work/j/jandrea/ProdHNL/CLICPerformance/fcceeConfig/config_values.py ."+"\n")
      file.write("cp /afs/cern.ch/work/j/jandrea/ProdHNL/CLICPerformance/fcceeConfig/fccRec_lcio_input.py ."+"\n")
      outputfileName = "HNL_50_"+str(ijob)+"_REC_EDM4Hep.root"
      arguments = " --LcioEvent.Files " + args.inputFiles +"/"+args.Sample+"/"+args.Sample+"_"+str(ijob)+"_evts.slcio --filename.PodioOutput  " + outputfileName+ " -n " + args.Nevts_per_job
      command = "k4run fccRec_lcio_input.py " + arguments
      file.write(command+"\n")
      file.write("cp "+ outputfileName + "  " + args.output_edm4hep+"_"+args.Sample+"_RECO_EDM4Hep"+"/."+"\n")
      file.close()
	
   condor_file = directory_job + "/condor_script.sub"
   print(condor_file)
   with open(condor_file, "w") as file2:
        file2.write("executable = bash_script.sh \n")
        file2.write("arguments = $(ClusterId) $(ProcId) \n")
        file2.write("output = output.$(ClusterId).$(ProcId).out \n")
        file2.write("error = error.$(ClusterId).$(ProcId).err \n")
        file2.write("log = log.$(ClusterId).log \n")
        #file2.write("+JobFlavour = \"espresso\" \n")
        #file2.write("+JobFlavour = \"microcentury\" \n")
        file2.write("+JobFlavour = \"longlunch\" \n")
        file2.write("queue \n")
        file2.close()
   os.system("cd "+ directory_job + "; condor_submit condor_script.sub")






