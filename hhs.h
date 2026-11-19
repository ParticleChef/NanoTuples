cmsDriver.py --scenario pp --era Run3_2024 \
  --customise Configuration/DataProcessing/Utils.addMonitoring,PhysicsTools/NanoAK15/ak15_cff.nanoAK15_customizeMC \
  --step NANO \
  --conditions 150X_mcRun3_2024_realistic_v2 \
  --datatier NANOAODSIM --eventcontent NANOAODSIM \
  --python_filename nanoaod_cfg.py \
  --fileout file:nanoaod.root \
  --filein /store/mc/RunIII2024Summer24MiniAODv6/QCDB-4Jets_Bin-HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/100000/00d1f84c-5b91-42d7-968a-5290825ecfaa.root \
  --no_exec --mc -n 9999

cmsRun nanoaod_cfg.py
