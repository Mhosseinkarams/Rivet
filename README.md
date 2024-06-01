# Rivet Analysis Repository

This repository contains my Rivet analysis using the Rivet package. Below are the steps to set up the environment and run the analysis.

## Prerequisites

Follow the setup instructions provided in the [CMS-Gen Rivet repository](https://gitlab.cern.ch/cms-gen/Rivet) to configure your environment on lxplus7.

## Environment Setup

1. First, create a personal fork of the CMS-Gen Rivet repository:
   - [Fork the repository](https://gitlab.cern.ch/cms-gen/Rivet/-/forks/new)

2. Set up your CMSSW environment:

    ```sh
    cmsrel CMSSW_11_2_4
    cd CMSSW_11_2_4/src
    cmsenv
    ```

3. Merge the required topic:

    ```sh
    git cms-merge-topic mseidel42:RivetPaths_11_2
    ```

4. Clone your fork of the Rivet repository:

    ```sh
    git clone ssh://git@gitlab.cern.ch:7999/${USER}/Rivet.git
    cd Rivet
    git remote add cms-gen ssh://git@gitlab.cern.ch:7999/cms-gen/Rivet.git
    git pull cms-gen master
    ```

5. Source the Rivet setup script and build the environment:

    ```sh
    source rivetSetup.sh
    scram b -j8
    ```

6. For using this repository, delete all groups folders and copy the `SMP` folder from this repository into the `Rivet` directory before running `scram b -j8` again.

## Running the Analysis

### Locally

To run the code locally, use the following command:

```sh
cmsRun runRivetAnalyzer_VJJ_miniAOD2016pre.py
```

### On CRAB

1. Activate your VOMS proxy:

    ```sh
    voms-proxy-init -voms cms
    ```

2. Submit the job on CRAB:

    ```sh
    crab submit --config crab_cfg2016pre.py General.requestName=GJets_SM_5f_TuneCP5_EWK_2016pre Data.inputDataset=/GJets_SM_5f_TuneCP5_EWK_dipoleRecoil_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM General.workArea=GJets_SM_5f_TuneCP5_EWK_2016pre
    ```
### Dataset Configuration

For each dataset ("2016pre", "2016post", "2017", "2018"), there is a corresponding CRAB configuration file and a `.cc` file. The `.cc` files, responsible for the main Rivet analysis, are located in the `SMP/src` directory. Each analysis has different source files:

- **2016pre dataset**: `CMS_1601_PAS_SMP_19_005`
- **2016post dataset**: `CMS_1602_PAS_SMP_19_005`
- **2017 dataset**: `CMS_2017_PAS_SMP_19_005`
- **2018 dataset**: `CMS_2018_PAS_SMP_19_005`

Each Rivet analysis has its own source files located in both `SMP/data` and `SMP/src`. It is recommended to keep these two directories in sync.


## Output Handling

The outputs of the CRAB jobs can be found in the following directory:

```
/eos/cms/store/group/phys_smp/vbfA/Mhossein_Rivet_test
```

### Merging Output Files

To merge the output files, you can use:

```sh
rivet-merge -e [first.yoda] [second.yoda] ... -o [merged.yoda]
```

Or for easier use:

```sh
rivet-merge -e *.yoda -o [merged.yoda]
```

### Plotting and Conversion

To draw the plots:

```sh
rivet-mkhtml --no-weight [file.yoda]
```

To convert to a ROOT file:

```sh
yoda2root [input.yoda] [output.root]
```

## Generating .yoda Files

As this analysis is for a paper that is not yet published, you need to create your own `.yoda` source file using the `root_to_yoda.ipynb` file in the `Handling_yoda` directory.

## Contact

For any issues or questions, please contact M.H Karam Sichani at mkaramsi@cern.ch.

---

Follow the steps carefully to set up your environment and run the analysis. If you encounter any problems, feel free to reach out for support.
