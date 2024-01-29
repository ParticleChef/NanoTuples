import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var


def getCustomTaggerDiscriminatorsAK8(process, name):
    customTaggersAvailableDict = {
        'InclParticleTransformerV2': {
            'cff_path': 'PhysicsTools.NanoTuples.taggingTools.pfMassDecorrelatedInclParticleTransformerV2_cff',
            'disc_name': '_pfMassDecorrelatedInclParticleTransformerV2JetTagsAll',
            'nano_branch_name': 'ParT',
        },
    }
    if name not in customTaggersAvailableDict:
        raise ValueError("the specified tagger '%s' does not exist." % name)

    cfg = customTaggersAvailableDict[name]
    mod = __import__(cfg['cff_path'], globals(), locals(), [cfg['disc_name']])
    btagDiscriminators = getattr(mod, cfg['disc_name'])

    # add variables to NanoAOD FatJet table
    for prob in btagDiscriminators:  # include all raw scores and tagger discriminants
        name = cfg['nano_branch_name'] + '_' + prob.split(':')[1]
        setattr(process.fatJetTable.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    return btagDiscriminators


def addCustomTaggerAK8(process, customAK8Taggers):
    tag_discs = sum([getCustomTaggerDiscriminatorsAK8(process, name) for name in customAK8Taggers], [])

    from PhysicsTools.NanoTuples.taggingTools.jetCustomTools import updateJetCollection
    JETCorrLevels = ['L2Relative', 'L3Absolute', 'L2L3Residual']
    # inference the tagger score
    updateJetCollection(
        process,
        jetSource=cms.InputTag('selectedUpdatedPatJetsAK8WithDeepInfo'),
        rParam=0.8,
        jetCorrections=('AK8PFPuppi', cms.vstring(JETCorrLevels), 'None'),
        btagDiscriminators=tag_discs,
        postfix='AK8WithCustomTagger',
    )
    process.jetCorrFactorsAK8.src = "selectedUpdatedPatJetsAK8WithCustomTagger"
    process.updatedJetsAK8.jetSource = "selectedUpdatedPatJetsAK8WithCustomTagger"
