#! /bin/bash

# Run3: https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis#Year_2023

# 2022: https://docs.google.com/presentation/d/1F4ndU7DBcyvrEEyLfYqb29NGkBPs20EAnBxe_l7AEII/edit#slide=id.g289f499aa6b_2_52

# 2023: https://docs.google.com/presentation/d/1TjPem5jX0fzqvTGl271_nQFoVBabsrdrO0i8Qo1uD5E/edit#slide=id.g289f499aa6b_2_58

###### MC ######

# MC, Summer22
cmsDriver.py mc_2022_preEE --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --fileout file:nano.root --conditions 133X_mcRun3_2022_realistic_ForNanov13_v1 --step NANO --filein file:inMINIAOD.root --era Run3 --no_exec -n -1

# MC, Summer22EE
cmsDriver.py mc_2022_postEE --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --fileout file:nano.root --conditions 133X_mcRun3_2022_realistic_postEE_ForNanov13_v1 --step NANO --filein file:inMINIAOD.root --era Run3 --no_exec -n -1

# MC, Summer23
cmsDriver.py mc_2023_preBPix --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --fileout file:nano.root --conditions 133X_mcRun3_2023_realistic_ForNanov13_v1 --step NANO --filein file:inMINIAOD.root --era Run3_2023 --no_exec -n -1

# MC, Summer23BPix
cmsDriver.py mc_2023_postBPix --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --fileout file:nano.root --conditions 133X_mcRun3_2023_realistic_postBPix_ForNanov13_v2 --step NANO --filein file:inMINIAOD.root --era Run3_2023 --no_exec -n -1

###### DATA ######

# Data, Run2022C,D,E
cmsDriver.py data_2022CDE --data --eventcontent NANOAOD --datatier NANOAOD --fileout file:nano.root --conditions 133X_dataRun3_ForNanov13_v1 --step NANO --filein file:inMINIAOD.root --era Run3 --customise PhysicsTools/NanoAOD/nano_cff.nanoL1TrigObjCustomize --no_exec -n -1

# Data, Run2022F,G
cmsDriver.py data_2022FG --data --eventcontent NANOAOD --datatier NANOAOD --fileout file:nano.root --conditions 133X_dataRun3_PromptAnalysis_ForNanov13_v1 --step NANO --filein file:inMINIAOD.root --era Run3 --customise PhysicsTools/NanoAOD/nano_cff.nanoL1TrigObjCustomize --no_exec -n -1

# Data, Run2023C,D
cmsDriver.py data_2023CD --data --eventcontent NANOAOD --datatier NANOAOD --fileout file:nano.root --conditions 133X_dataRun3_Prompt_ForNanov13_v2 --step NANO --filein file:inMINIAOD.root --era Run3 --customise PhysicsTools/NanoAOD/nano_cff.nanoL1TrigObjCustomize --no_exec -n -1

for cfg in $(ls *_202*.py); do
    echo "Adding ParticleNetAK8 raw scores to ${cfg}"
    sed -i -e 's@# Customisation from command line@# Customisation from command line\nfrom RecoBTag.ONNXRuntime.pfParticleNetFromMiniAODAK8_cff import _pfParticleNetFromMiniAODAK8JetTagsProbs\nfrom PhysicsTools.NanoAOD.common_cff import Var\nfor prob in _pfParticleNetFromMiniAODAK8JetTagsProbs:\n    name = "ParticleNet_raw_" + prob.split(":")[1]\n    setattr(process.fatJetTable.variables, name, Var("bDiscriminator('"'"'%s'"'"')" % prob, float, doc=prob, precision=-1))\n@' ${cfg}

    echo "Adding ParticleNetAK4 Run2UL to ${cfg}"
    sed -i -e 's@# Customisation from command line@# Customisation from command line\nfrom RecoBTag.ONNXRuntime.pfParticleNetAK4_cff import _pfParticleNetAK4JetTagsProbs\nfrom PhysicsTools.NanoAOD.common_cff import Var\nfor prob in _pfParticleNetAK4JetTagsProbs:\n    name = "ParticleNetAK4_" + prob.split(":")[1]\n    setattr(process.jetPuppiTable.variables, name, Var("bDiscriminator('"'"'%s'"'"')" % prob, float, doc=prob, precision=-1))\n@' ${cfg}
done

for cfg in $(ls mc_202*.py); do
    echo "Adding AK4 nBHadrons/nCHadrons to ${cfg}"
    sed -i -e 's@# Customisation from command line@# Customisation from command line\nfrom PhysicsTools.NanoAOD.common_cff import Var\nprocess.jetMCTable.variables.nBHadrons = Var("jetFlavourInfo().getbHadrons().size()", "uint8", doc="number of b-hadrons")\nprocess.jetMCTable.variables.nCHadrons = Var("jetFlavourInfo().getcHadrons().size()", "uint8", doc="number of c-hadrons")\n@' ${cfg}
done

for cfg in $(ls data_202*.py); do
    echo "Adding nanoTuples_customizeData to ${cfg}"
    sed -i -e 's@# Customisation from command line@# Customisation from command line\nfrom PhysicsTools.NanoTuples.nanoTuples_cff import nanoTuples_customizeData\nprocess = nanoTuples_customizeData(process)\n@' ${cfg}
done

for cfg in $(ls mc_202*.py); do
    echo "Adding nanoTuples_customizeMC to ${cfg}"
    sed -i -e 's@# Customisation from command line@# Customisation from command line\nfrom PhysicsTools.NanoTuples.nanoTuples_cff import nanoTuples_customizeMC\nprocess = nanoTuples_customizeMC(process)\n@' ${cfg}
done
