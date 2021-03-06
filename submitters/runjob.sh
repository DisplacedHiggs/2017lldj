#!/bin/bash

export PATH=${PATH}:/cvmfs/cms.cern.ch/common
export CMS_PATH=/cvmfs/cms.cern.ch

#get the release setup and in place
#CMSSW_RELEASE_BASE="/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw-patch/CMSSW_8_0_26_patch1"

export SCRAM_ARCH=slc7_amd64_gcc630
scramv1 project CMSSW CMSSW_9_4_10

cd CMSSW_9_4_10
cd src
printf "pwd\n"
pwd

cp ../../2017_puWeights_DoubleEG_69200.root          .
cp ../../2017_puWeights_DoubleMuon_69200.root          .
cp ../../2017_puWeights_MuonEG_69200.root            .
cp ../../2017_ElectronTight.root     .
cp ../../2017_ElectronMedium.root    .
cp ../../2017_ElectronLoose.root     .
cp ../../RunBCDEF_SF_ID.root     .
cp ../../RunBCDEF_SF_ISO.root     .
cp ../../feff_ZH.root                           .


scramv1 build -j 10
eval `scramv1 runtime -sh` # cmsenv

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${PWD}

printf "ls -lhrt \n"
ls -lhrt

printf "ls -lhrt ../ \n"
ls -lhrt ../

printf "ls -lhrt ../../ \n"
ls -lhrt ../../

../../runanalyzer.exe -s $1 -l $2 -e $3  -i "../.." -o "../.." -n $4 -a $5 -x $6 $7

printf "ls -lhrt \n"
ls -lhrt

printf "ls -lhrt ../ \n"
ls -lhrt ../

printf "ls -lhrt ../../ \n"
ls -lhrt ../../

