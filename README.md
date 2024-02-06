# NanoTuples

Custom NanoAOD ntuple producers with additional boosted jet taggers and their PF candidates.

<!-- TOC -->

- [NanoTuples](#nanotuples)
    - [Version](#version)
    - [Setup](#setup)
    - [Production](#production)

<!-- /TOC -->

---

## Version

The current version is based on the Run2UL config in CMSSW_13_3_1_patch1, so it is a mixture of [NanoAODv9](https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Releases/NanoAODv9) and [NanoAODv13](https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Releases/NanoAODv13).

Customizations:

- Switched to Puppi jets for the AK4 jet collection.
- Add the Run2UL version of ParticleNetAK4 (trained on CHS jets) on AK4 Puppi jets.
- Add the new Run3 ParticleNetAK4 tagger (with regression) and the RobustParTAK4 tagger.
<!-- - Add the new Run3 ParticleNetAK4-based tau taggers. -->
- Store all ParticleNet raw scores for AK8 jets.
- Add new GlobalParT stage-2 for AK8 jets.
- Add new GlobalParT stage-2 for AK15 jets.
- AK15 jets w/ ParticleNet-MD (V02d, EOY training) and mass regression (V01c, EOY training).

---

## Setup

```bash
cmsrel CMSSW_13_3_1_patch1
cd CMSSW_13_3_1_patch1/src
cmsenv

# merge custom CMSSW branch for AK4Puppi
git cms-merge-topic -u hqucms:dev/CMSSW_13_3_1_patch1/NanoAOD-puppiAK4

# add custom repo for AK15/AK8 ParTv2
git clone ssh://git@gitlab.cern.ch:7999/cms-hcc/NanoTuples.git PhysicsTools/NanoTuples -b dev/ParTv2/CMSSW_13_3_1_patch1

# compile
scram b -j8
cmsenv
```

## Production

**Step 0**: switch to the crab production directory and set up grid proxy, CRAB environment, etc.

```bash
# set up grid proxy
voms-proxy-init -rfc -voms cms --valid 168:00
# set up CRAB env (must be done after cmsenv)
source /cvmfs/cms.cern.ch/common/crab-setup.sh
```

**Step 1**: generate the python config file with `generateConfigs.sh`.

**Step 2**: use the `crab.py` script to submit the CRAB jobs:

For MC:

```bash
crab.py -p mc_2018UL_NANO.py --max-memory 2500 --site T2_CH_CERN -o /store/group/cmst3/group/vhcc/NanoAOD/dev_AK15_ParTv2/2018/mc -t NanoTuples-06Feb2024_Run2UL_AK4Puppi_AK15_ParTv2 -i mc/mc_2018.conf --num-cores 1 -s FileBased -n 2 --work-area crab_projects_2018UL --dryrun

crab.py -p mc_2017UL_NANO.py --max-memory 2500 --site T2_CH_CERN -o /store/group/cmst3/group/vhcc/NanoAOD/dev_AK15_ParTv2/2017/mc -t NanoTuples-06Feb2024_Run2UL_AK4Puppi_AK15_ParTv2 -i mc/mc_2017.conf --num-cores 1 -s FileBased -n 2 --work-area crab_projects_2017UL --dryrun

crab.py -p mc_2016ULpostVFP_NANO.py --max-memory 2500 --site T2_CH_CERN -o /store/group/cmst3/group/vhcc/NanoAOD/dev_AK15_ParTv2/2016/mc -t NanoTuples-06Feb2024_Run2UL_AK4Puppi_AK15_ParTv2 -i mc/mc_2016post.conf --num-cores 1 -s FileBased -n 2 --work-area crab_projects_2016ULpostVFP --dryrun

crab.py -p mc_2016ULpreVFP_NANO.py --max-memory 2500 --site T2_CH_CERN -o /store/group/cmst3/group/vhcc/NanoAOD/dev_AK15_ParTv2/2016APV/mc -t NanoTuples-06Feb2024_Run2UL_AK4Puppi_AK15_ParTv2 -i mc/mc_2016pre.conf --num-cores 1 -s FileBased -n 2 --work-area crab_projects_2016ULpreVFP --dryrun
```

For Data:

```bash
crab.py -p data_2018UL_NANO.py --max-memory 2500 --site T2_CH_CERN -o /store/group/cmst3/group/vhcc/NanoAOD/dev_AK15_ParTv2/2018/data -t NanoTuples-06Feb2024_Run2UL_AK4Puppi_AK15_ParTv2 -i data/data_2018.conf --num-cores 1 -s EventAwareLumiBased -n 100000 -j 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt' --work-area crab_projects_data_2018UL --dryrun

crab.py -p data_2017UL_NANO.py --max-memory 2500 --site T2_CH_CERN -o /store/group/cmst3/group/vhcc/NanoAOD/dev_AK15_ParTv2/2017/data -t NanoTuples-06Feb2024_Run2UL_AK4Puppi_AK15_ParTv2 -i data/data_2017.conf --num-cores 1 -s EventAwareLumiBased -n 100000 -j 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt' --work-area crab_projects_data_2017UL --dryrun

crab.py -p data_2016ULpostVFP_NANO.py --max-memory 2500 --site T2_CH_CERN -o /store/group/cmst3/group/vhcc/NanoAOD/dev_AK15_ParTv2/2016/data -t NanoTuples-06Feb2024_Run2UL_AK4Puppi_AK15_ParTv2 -i data/data_2016post.conf --num-cores 1 -s EventAwareLumiBased -n 100000 -j 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt' --work-area crab_projects_data_2016ULpostVFP --dryrun

crab.py -p data_2016ULpreVFP_NANO.py --max-memory 2500 --site T2_CH_CERN -o /store/group/cmst3/group/vhcc/NanoAOD/dev_AK15_ParTv2/2016APV/data -t NanoTuples-06Feb2024_Run2UL_AK4Puppi_AK15_ParTv2 -i data/data_2016pre.conf --num-cores 1 -s EventAwareLumiBased -n 100000 -j 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt' --work-area crab_projects_data_2016ULpreVFP --dryrun
```

These commands will perform a "dryrun" to print out the CRAB configuration files. Please check everything is correct (e.g., the output path, version number, requested number of cores, etc.) before submitting the actual jobs. To actually submit the jobs to CRAB, just remove the `--dryrun` option at the end.

**Step 3**: check job status

The status of the CRAB jobs can be checked with:

```bash
./crab.py --status --work-area crab_projects_*  --options "maxjobruntime=2500 maxmemory=2500" && ./crab.py --summary
```

Note that this will also **resubmit** failed jobs automatically.

The crab dashboard can also be used to get a quick overview of the job status:

- [https://monit-grafana.cern.ch/d/cmsTMGlobal/cms-tasks-monitoring-globalview?orgId=11](https://monit-grafana.cern.ch/d/cmsTMGlobal/cms-tasks-monitoring-globalview?orgId=11)

More options of this `crab.py` script can be found with:

```bash
./crab.py -h
```
