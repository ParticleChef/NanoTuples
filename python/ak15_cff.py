"""AK15 Puppi jets for NanoAODv15 (CMSSW_15_0_X).

Port of NanoTuples dev/ParTv2/CMSSW_13_3_1_patch1 python/ak15_cff.py. Same chain, same table
names and branch names:  AK15Puppi, AK15PuppiSubJet, GenJetAK15, GenSubJetAK15.

Changes w.r.t. the original (all forced by differences between CMSSW 13_3_1_patch1 + the
topic branch and official 15_0_X):
  1. ParTv2 is attached with partV2.addParTv2Tagger() instead of being requested through
     updateJetCollection (v15's jetTools has no pfParticleTransformerAK8TagInfos branch).
  2. The jet tables use simplePATJetFlatTableProducer (as the v15 FatJet/SubJet tables do)
     instead of SimpleCandidateFlatTableProducer. Variable expressions are unchanged.
  3. The Run2UL jet-ID value maps are optional (addJetID=False by default); the 'RUN2ULPUPPI'
     PatJetIDValueMapProducer version could not be confirmed to exist in v15. When off, the
     'jetId' branch is not written.
"""
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.simplePATJetFlatTableProducer_cfi import simplePATJetFlatTableProducer
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
from RecoBTag.ONNXRuntime.pfParticleNet_cff import _pfMassDecorrelatedParticleNetJetTagsProbs, _pfParticleNetMassRegressionOutputs

from PhysicsTools.NanoTuples.jetUtils import addCustomJets
from PhysicsTools.NanoTuples.partV2 import addParTv2Tagger, getParTv2Branches

_UPDATE_POSTFIX = 'AK15ParticleNet'


def _require(process, label, hint=''):
    if not hasattr(process, label):
        raise RuntimeError("setupAK15: expected module '%s' was not created by updateJetCollection. %s" % (label, hint))
    return getattr(process, label)


def setupAK15(process, runOnMC=False, path=None, runParticleNetMD=True, customAK15Taggers=[], addJetID=False):
    # cluster AK15Puppi jets (reco + gen, soft-drop, subjets) from packedPFCandidates
    addCustomJets(process, rParam=1.5, jetAlgo='ak15', minPt=150, runOnMC=runOnMC)

    bTagDiscriminators = []
    JETCorrLevels = ['L2Relative', 'L3Absolute', 'L2L3Residual']
    if runParticleNetMD:
        bTagDiscriminators += _pfMassDecorrelatedParticleNetJetTagsProbs + _pfParticleNetMassRegressionOutputs

    updateJetCollection(
        process,
        jetSource=cms.InputTag('packedPatJetsAK15PFPuppiSoftDrop'),
        rParam=1.5,
        jetCorrections=('AK8PFPuppi', cms.vstring(JETCorrLevels), 'None'),
        btagDiscriminators=bTagDiscriminators if len(bTagDiscriminators) > 0 else ['None'],
        postfix=_UPDATE_POSTFIX,
    )

    if runParticleNetMD:
        hint = "Compare the module names in the v15 jetTools.updateJetCollection output."
        _require(process, 'pfParticleNetTagInfos' + _UPDATE_POSTFIX, hint).jet_radius = 1.5
        mdTagger = _require(process, 'pfMassDecorrelatedParticleNetJetTags' + _UPDATE_POSTFIX, hint)
        mdTagger.preprocess_json = 'PhysicsTools/NanoTuples/data/ParticleNet-MD/ak15/V02d/preprocess.json'
        mdTagger.model_path = 'PhysicsTools/NanoTuples/data/ParticleNet-MD/ak15/V02d/particle-net.onnx'
        massReg = _require(process, 'pfParticleNetMassRegressionJetTags' + _UPDATE_POSTFIX, hint)
        massReg.preprocess_json = 'PhysicsTools/NanoTuples/data/MassRegression/ak15/V01c/preprocess.json'
        massReg.model_path = 'PhysicsTools/NanoTuples/data/MassRegression/ak15/V01c/particle_net_regression.onnx'

    # custom AK15 taggers (ParTv2): own tag-info + ONNX modules, scores embedded in the updater
    parBranches = []
    for name in customAK15Taggers:
        addParTv2Tagger(process, updater='updatedPatJets' + _UPDATE_POSTFIX, jetRadius=1.5, name=name, suffix='AK15')
        parBranches += getParTv2Branches(name)

    # src
    srcJets = cms.InputTag('selectedUpdatedPatJets' + _UPDATE_POSTFIX)

    # jetID (optional, see module docstring)
    userInts = cms.PSet()
    if addJetID:
        process.tightJetIdAK15Puppi = cms.EDProducer("PatJetIDValueMapProducer",
            filterParams=cms.PSet(
                version=cms.string('RUN2ULPUPPI'),
                quality=cms.string('TIGHT'),
            ),
            src=srcJets
        )
        process.tightJetIdLepVetoAK15Puppi = cms.EDProducer("PatJetIDValueMapProducer",
            filterParams=cms.PSet(
                version=cms.string('RUN2ULPUPPI'),
                quality=cms.string('TIGHTLEPVETO'),
            ),
            src=srcJets
        )
        userInts = cms.PSet(
            tightId=cms.InputTag("tightJetIdAK15Puppi"),
            tightIdLepVeto=cms.InputTag("tightJetIdLepVetoAK15Puppi"),
        )

    process.ak15WithUserData = cms.EDProducer("PATJetUserDataEmbedder",
        src=srcJets,
        userFloats=cms.PSet(),
        userInts=userInts,
    )

    process.ak15Table = simplePATJetFlatTableProducer.clone(
        src=cms.InputTag("ak15WithUserData"),
        name=cms.string("AK15Puppi"),
        cut=cms.string(""),
        doc=cms.string("ak15 puppi jets"),
        variables=cms.PSet(P4Vars,
            area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
            rawFactor=Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=6),
            # nPFConstituents=Var("numberOfDaughters()", int, doc="Number of PF candidate constituents"),
            tau1=Var("userFloat('NjettinessAK15Puppi:tau1')", float, doc="Nsubjettiness (1 axis)", precision=10),
            tau2=Var("userFloat('NjettinessAK15Puppi:tau2')", float, doc="Nsubjettiness (2 axis)", precision=10),
            tau3=Var("userFloat('NjettinessAK15Puppi:tau3')", float, doc="Nsubjettiness (3 axis)", precision=10),
            msoftdrop=Var("groomedMass()", float, doc="Corrected soft drop mass with PUPPI", precision=10),
            nBHadrons=Var("jetFlavourInfo().getbHadrons().size()", int, doc="number of b-hadrons"),
            nCHadrons=Var("jetFlavourInfo().getcHadrons().size()", int, doc="number of c-hadrons"),
            subJetIdx1=Var("?nSubjetCollections()>0 && subjets().size()>0?subjets()[0].key():-1", int,
                 doc="index of first subjet"),
            subJetIdx2=Var("?nSubjetCollections()>0 && subjets().size()>1?subjets()[1].key():-1", int,
                 doc="index of second subjet"),
        )
    )
    if addJetID:
        process.ak15Table.variables.jetId = Var("userInt('tightId')*2+4*userInt('tightIdLepVeto')", int,
            doc="Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto")
    process.ak15Table.variables.pt.precision = 10

    if runParticleNetMD:
        for prob in _pfMassDecorrelatedParticleNetJetTagsProbs + _pfParticleNetMassRegressionOutputs:
            name = 'ParticleNetMD_' + prob.split(':')[1]
            setattr(process.ak15Table.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    # add other AK15 custom taggers
    for name, var_info in parBranches:
        setattr(process.ak15Table.variables, name, var_info)

    process.ak15SubJetTable = simplePATJetFlatTableProducer.clone(
        src=cms.InputTag("selectedPatJetsAK15PFPuppiSoftDropPacked", "SubJets"),
        cut=cms.string(""),
        name=cms.string("AK15PuppiSubJet"),
        doc=cms.string("ak15 puppi subjets"),
        variables=cms.PSet(P4Vars,
            area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
            rawFactor=Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=6),
            nBHadrons=Var("jetFlavourInfo().getbHadrons().size()", int, doc="number of b-hadrons"),
            nCHadrons=Var("jetFlavourInfo().getcHadrons().size()", int, doc="number of c-hadrons"),
        )
    )
    process.ak15SubJetTable.variables.pt.precision = 10

    process.ak15Task = cms.Task(
        process.ak15WithUserData,
        process.ak15Table,
        process.ak15SubJetTable,
    )
    if addJetID:
        process.ak15Task.add(process.tightJetIdAK15Puppi, process.tightJetIdLepVetoAK15Puppi)

    if runOnMC:
        process.genJetAK15Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
            src=cms.InputTag("ak15GenJetsNoNu"),
            cut=cms.string("pt > 100."),
            name=cms.string("GenJetAK15"),
            doc=cms.string("AK15 GenJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.genJetAK15Table.variables.pt.precision = 10

        process.genSubJetAK15Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
            src=cms.InputTag("ak15GenJetsNoNuSoftDrop", "SubJets"),
            cut=cms.string(""),
            name=cms.string("GenSubJetAK15"),
            doc=cms.string("AK15 Gen-SubJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.genSubJetAK15Table.variables.pt.precision = 10

        process.ak15Task.add(process.genJetAK15Table)
        process.ak15Task.add(process.genSubJetAK15Table)
        ###############################################

    if path is None:
        process.schedule.associate(process.ak15Task)
    else:
        getattr(process, path).associate(process.ak15Task)
