#!/bin/env bash

cd ../../../
echo $PWD
eval `scramv1 runtime -sh`;
/cvmfs/cms.cern.ch/common/scram b;

echo $PWD
