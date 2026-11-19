"""ParTv2 (InclParticleTransformer-MD) tag-info producer + ONNX tagger definitions.

Transplanted from hqucms:dev/CMSSW_13_3_1_patch1/NanoAOD-puppiAK4
(RecoBTag/ONNXRuntime/python/pfParticleTransformerAK8_cff.py) into this package, because
official CMSSW (13_3_X ... 15_0_X ... master) does not contain it. Official v15 ships
GlobalParT (pfGlobalParticleTransformerAK8_cff) instead, which is a different tagger.

Differences w.r.t. the original:
  * the tag-info producer is defined explicitly here (all parameters of the plugin's
    fillDescriptions), so no auto-generated *_cfi.py is needed;
  * the plugin lives in PhysicsTools/NanoTuples/plugins, not RecoBTag/FeatureTools;
  * it is NOT registered in RecoBTag/PatAlgos supportedBtagDiscr (that needed edits to
    jetTools.py / bTagging_cff.py); see partV2.py for how the scores are attached instead.
"""
import FWCore.ParameterSet.Config as cms
from RecoBTag.ONNXRuntime.boostedJetONNXJetTagsProducer_cfi import boostedJetONNXJetTagsProducer

pfParticleTransformerAK8TagInfos = cms.EDProducer("ParticleTransformerAK8TagInfoProducer",
    jet_radius = cms.double(0.8),
    min_jet_pt = cms.double(150),
    max_jet_eta = cms.double(99),
    min_pt_for_track_properties = cms.double(-1),
    min_puppi_wgt = cms.double(0.01),
    flip_ip_sign = cms.bool(False),
    sip3dSigMax = cms.double(-1),
    vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    secondary_vertices = cms.InputTag("slimmedSecondaryVertices"),
    pf_candidates = cms.InputTag("packedPFCandidates"),
    lost_tracks = cms.InputTag("lostTracks"),
    jets = cms.InputTag("slimmedJetsAK8"),
    puppi_value_map = cms.InputTag("packedpuppi"),
    vertex_associator = cms.InputTag(""),
)

pfParticleTransformerAK8MDJetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleTransformerAK8TagInfos',
    # placeholders: partV2.addParTv2Tagger() always overrides both with the AK8/AK15 model
    preprocess_json = 'PhysicsTools/NanoTuples/data/InclParticleTransformer-MD/ak8/V02/preprocess_corr.json',
    model_path = 'PhysicsTools/NanoTuples/data/InclParticleTransformer-MD/ak8/V02/model.onnx',
    flav_names = [
        'probTopbWcs', 'probTopbWqq', 'probTopbWc', 'probTopbWs', 'probTopbWq', 'probTopbWev', 'probTopbWmv', 'probTopbWtauev', 'probTopbWtaumv', 'probTopbWtauhv', 
        'probTopWcs', 'probTopWqq', 'probTopWev', 'probTopWmv', 'probTopWtauev', 'probTopWtaumv', 'probTopWtauhv', 
        'probHbb', 'probHcc', 'probHss', 'probHqq', 'probHbc', 'probHbs', 'probHcs', 'probHgg', 'probHee', 'probHmm', 'probHtauhtaue', 'probHtauhtaum', 'probHtauhtauh', 
        'probHWWcscs', 'probHWWcsqq', 'probHWWqqqq', 'probHWWcsc', 'probHWWcss', 'probHWWcsq', 'probHWWqqc', 'probHWWqqs', 'probHWWqqq', 
        'probHWWcsev', 'probHWWqqev', 'probHWWcsmv', 'probHWWqqmv', 'probHWWcstauev', 'probHWWqqtauev', 'probHWWcstaumv', 'probHWWqqtaumv', 'probHWWcstauhv', 'probHWWqqtauhv', 
        'probHWxWxcscs', 'probHWxWxcsqq', 'probHWxWxqqqq', 'probHWxWxcsc', 'probHWxWxcss', 'probHWxWxcsq', 'probHWxWxqqc', 'probHWxWxqqs', 'probHWxWxqqq', 
        'probHWxWxcsev', 'probHWxWxqqev', 'probHWxWxcsmv', 'probHWxWxqqmv', 'probHWxWxcstauev', 'probHWxWxqqtauev', 'probHWxWxcstaumv', 'probHWxWxqqtaumv', 'probHWxWxcstauhv', 'probHWxWxqqtauhv', 
        'probHWxWxStarcscs', 'probHWxWxStarcsqq', 'probHWxWxStarqqqq', 'probHWxWxStarcsc', 'probHWxWxStarcss', 'probHWxWxStarcsq', 'probHWxWxStarqqc', 'probHWxWxStarqqs', 'probHWxWxStarqqq', 
        'probHWxWxStarcsev', 'probHWxWxStarqqev', 'probHWxWxStarcsmv', 'probHWxWxStarqqmv', 'probHWxWxStarcstauev', 'probHWxWxStarqqtauev', 'probHWxWxStarcstaumv', 'probHWxWxStarqqtaumv', 'probHWxWxStarcstauhv', 'probHWxWxStarqqtauhv', 
        'probHZZbbbb', 'probHZZbbcc', 'probHZZbbss', 'probHZZbbqq', 'probHZZcccc', 'probHZZccss', 'probHZZccqq', 'probHZZssss', 'probHZZssqq', 'probHZZqqqq', 'probHZZbbb', 'probHZZbbc', 'probHZZbbs', 'probHZZbbq', 'probHZZccb', 'probHZZccc', 'probHZZccs', 'probHZZccq', 'probHZZssb', 'probHZZssc', 'probHZZsss', 'probHZZssq', 'probHZZqqb', 'probHZZqqc', 'probHZZqqs', 'probHZZqqq', 
        'probHZZbbee', 'probHZZbbmm', 'probHZZbbe', 'probHZZbbm', 'probHZZbee', 'probHZZbmm', 'probHZZbbtauhtaue', 'probHZZbbtauhtaum', 'probHZZbbtauhtauh', 'probHZZbtauhtaue', 'probHZZbtauhtaum', 'probHZZbtauhtauh', 'probHZZccee', 'probHZZccmm', 'probHZZcce', 'probHZZccm', 'probHZZcee', 'probHZZcmm', 'probHZZcctauhtaue', 'probHZZcctauhtaum', 'probHZZcctauhtauh', 'probHZZctauhtaue', 'probHZZctauhtaum', 'probHZZctauhtauh', 'probHZZssee', 'probHZZssmm', 'probHZZsse', 'probHZZssm', 'probHZZsee', 'probHZZsmm', 'probHZZsstauhtaue', 'probHZZsstauhtaum', 'probHZZsstauhtauh', 'probHZZstauhtaue', 'probHZZstauhtaum', 'probHZZstauhtauh', 'probHZZqqee', 'probHZZqqmm', 'probHZZqqe', 'probHZZqqm', 'probHZZqee', 'probHZZqmm', 'probHZZqqtauhtaue', 'probHZZqqtauhtaum', 'probHZZqqtauhtauh', 'probHZZqtauhtaue', 'probHZZqtauhtaum', 'probHZZqtauhtauh', 
        'probHZxZxbbbb', 'probHZxZxbbcc', 'probHZxZxbbss', 'probHZxZxbbqq', 'probHZxZxcccc', 'probHZxZxccss', 'probHZxZxccqq', 'probHZxZxssss', 'probHZxZxssqq', 'probHZxZxqqqq', 'probHZxZxbbb', 'probHZxZxbbc', 'probHZxZxbbs', 'probHZxZxbbq', 'probHZxZxccb', 'probHZxZxccc', 'probHZxZxccs', 'probHZxZxccq', 'probHZxZxssb', 'probHZxZxssc', 'probHZxZxsss', 'probHZxZxssq', 'probHZxZxqqb', 'probHZxZxqqc', 'probHZxZxqqs', 'probHZxZxqqq', 
        'probHZxZxbbee', 'probHZxZxbbmm', 'probHZxZxbbe', 'probHZxZxbbm', 'probHZxZxbee', 'probHZxZxbmm', 'probHZxZxbbtauhtaue', 'probHZxZxbbtauhtaum', 'probHZxZxbbtauhtauh', 'probHZxZxbtauhtaue', 'probHZxZxbtauhtaum', 'probHZxZxbtauhtauh', 'probHZxZxccee', 'probHZxZxccmm', 'probHZxZxcce', 'probHZxZxccm', 'probHZxZxcee', 'probHZxZxcmm', 'probHZxZxcctauhtaue', 'probHZxZxcctauhtaum', 'probHZxZxcctauhtauh', 'probHZxZxctauhtaue', 'probHZxZxctauhtaum', 'probHZxZxctauhtauh', 'probHZxZxssee', 'probHZxZxssmm', 'probHZxZxsse', 'probHZxZxssm', 'probHZxZxsee', 'probHZxZxsmm', 'probHZxZxsstauhtaue', 'probHZxZxsstauhtaum', 'probHZxZxsstauhtauh', 'probHZxZxstauhtaue', 'probHZxZxstauhtaum', 'probHZxZxstauhtauh', 'probHZxZxqqee', 'probHZxZxqqmm', 'probHZxZxqqe', 'probHZxZxqqm', 'probHZxZxqee', 'probHZxZxqmm', 'probHZxZxqqtauhtaue', 'probHZxZxqqtauhtaum', 'probHZxZxqqtauhtauh', 'probHZxZxqtauhtaue', 'probHZxZxqtauhtaum', 'probHZxZxqtauhtauh', 
        'probHZxZxStarbbbb', 'probHZxZxStarbbcc', 'probHZxZxStarbbss', 'probHZxZxStarbbqq', 'probHZxZxStarcccc', 'probHZxZxStarccss', 'probHZxZxStarccqq', 'probHZxZxStarssss', 'probHZxZxStarssqq', 'probHZxZxStarqqqq', 'probHZxZxStarbbb', 'probHZxZxStarbbc', 'probHZxZxStarbbs', 'probHZxZxStarbbq', 'probHZxZxStarccb', 'probHZxZxStarccc', 'probHZxZxStarccs', 'probHZxZxStarccq', 'probHZxZxStarssb', 'probHZxZxStarssc', 'probHZxZxStarsss', 'probHZxZxStarssq', 'probHZxZxStarqqb', 'probHZxZxStarqqc', 'probHZxZxStarqqs', 'probHZxZxStarqqq', 
        'probHZxZxStarbbee', 'probHZxZxStarbbmm', 'probHZxZxStarbbe', 'probHZxZxStarbbm', 'probHZxZxStarbee', 'probHZxZxStarbmm', 'probHZxZxStarbbtauhtaue', 'probHZxZxStarbbtauhtaum', 'probHZxZxStarbbtauhtauh', 'probHZxZxStarbtauhtaue', 'probHZxZxStarbtauhtaum', 'probHZxZxStarbtauhtauh', 'probHZxZxStarccee', 'probHZxZxStarccmm', 'probHZxZxStarcce', 'probHZxZxStarccm', 'probHZxZxStarcee', 'probHZxZxStarcmm', 'probHZxZxStarcctauhtaue', 'probHZxZxStarcctauhtaum', 'probHZxZxStarcctauhtauh', 'probHZxZxStarctauhtaue', 'probHZxZxStarctauhtaum', 'probHZxZxStarctauhtauh', 'probHZxZxStarssee', 'probHZxZxStarssmm', 'probHZxZxStarsse', 'probHZxZxStarssm', 'probHZxZxStarsee', 'probHZxZxStarsmm', 'probHZxZxStarsstauhtaue', 'probHZxZxStarsstauhtaum', 'probHZxZxStarsstauhtauh', 'probHZxZxStarstauhtaue', 'probHZxZxStarstauhtaum', 'probHZxZxStarstauhtauh', 'probHZxZxStarqqee', 'probHZxZxStarqqmm', 'probHZxZxStarqqe', 'probHZxZxStarqqm', 'probHZxZxStarqee', 'probHZxZxStarqmm', 'probHZxZxStarqqtauhtaue', 'probHZxZxStarqqtauhtaum', 'probHZxZxStarqqtauhtauh', 'probHZxZxStarqtauhtaue', 'probHZxZxStarqtauhtaum', 'probHZxZxStarqtauhtauh', 
        'probQCDbb', 'probQCDcc', 'probQCDb', 'probQCDc', 'probQCDothers', 
        'resonanceMassCorr', 'visiableMassCorr',
    ],
)

# declare all the discriminators
# mass-decorrelated: probs
_pfParticleTransformerAK8MDJetTagsProbs = ['pfParticleTransformerAK8MDJetTags:' + flav_name
                                           for flav_name in pfParticleTransformerAK8MDJetTags.flav_names]
# mass-decorrelated: meta-taggers
_pfParticleTransformerAK8MDJetTagsMetaDiscrs = []

_pfParticleTransformerAK8JetTagsAll = _pfParticleTransformerAK8MDJetTagsProbs + _pfParticleTransformerAK8MDJetTagsMetaDiscrs
