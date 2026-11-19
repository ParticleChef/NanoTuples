"""ParTv2 (InclParticleTransformer-MD) on the AK8 FatJet collection, v15 port.

Same behaviour as NanoTuples ak8_cff.py (branches ``FatJet_ParT_*``), but the tagger is
attached with partV2.addParTv2Tagger() instead of through updateJetCollection's tagger
registry (not available in official v15, see partV2.py).

Note: v15 already stores GlobalParT-3 (``FatJet_globalParT3_*``) and ParticleNet scores.
ParTv2 is an additional, different tagger kept here only to match NanoTuples.
"""
import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

from PhysicsTools.NanoTuples.partV2 import addParTv2Tagger, getParTv2Branches

_POSTFIX = 'AK8WithCustomTagger'


def addCustomTaggerAK8(process, customAK8Taggers):
    JETCorrLevels = ['L2Relative', 'L3Absolute', 'L2L3Residual']
    # nanoAOD_addDeepInfoAK8() (v15 jetsAK8_cff) deletes selectedUpdatedPatJetsAK8WithDeepInfo after
    # cloning it as 'slimmedJetsAK8'; either way 'slimmedJetsAK8' is the right input here.
    src = 'selectedUpdatedPatJetsAK8WithDeepInfo' if hasattr(
        process, 'selectedUpdatedPatJetsAK8WithDeepInfo') else 'slimmedJetsAK8'
    updateJetCollection(
        process,
        jetSource=cms.InputTag(src),
        rParam=0.8,
        jetCorrections=('AK8PFPuppi', cms.vstring(JETCorrLevels), 'None'),
        btagDiscriminators=['None'],  # ParTv2 is added explicitly below
        postfix=_POSTFIX,
    )

    for name in customAK8Taggers:
        addParTv2Tagger(process, updater='updatedPatJets' + _POSTFIX, jetRadius=0.8, name=name, suffix='AK8')
        # add variables to NanoAOD FatJet table
        for bname, var in getParTv2Branches(name):
            setattr(process.fatJetTable.variables, bname, var)

    process.jetCorrFactorsAK8.src = "selectedUpdatedPatJets" + _POSTFIX
    process.updatedJetsAK8.jetSource = "selectedUpdatedPatJets" + _POSTFIX
