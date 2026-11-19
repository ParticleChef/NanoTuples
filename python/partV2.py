"""Attach the ParTv2 (InclParticleTransformer-MD) tagger to a PAT jet updater.

Why this exists
---------------
In NanoTuples (CMSSW_13_3_1_patch1) ParTv2 was run through ``updateJetCollection`` after the
topic branch hqucms:dev/CMSSW_13_3_1_patch1/NanoAOD-puppiAK4 had patched two CMSSW files:
  * PhysicsTools/PatAlgos/python/recoLayer0/bTagging_cff.py  (register tag infos + discriminators)
  * PhysicsTools/PatAlgos/python/tools/jetTools.py           (create pfParticleTransformerAK8TagInfos)
Official v15 has no such branch in ``jetTools.setupBTagging`` (only pfParticleNetTagInfos and
pfGlobalParticleTransformerAK8TagInfos), and we do not want to patch CMSSW. So the two
modules (tag infos + ONNX tagger) are created explicitly here and their outputs are added to
the ``discriminatorSources`` of the PATJetUpdater that ``updateJetCollection`` already made.

Naming
------
PATJetUpdater trims everything after "JetTags" in a discriminator module label. A module
called ``pfParticleTransformerAK8MDJetTags<suffix>`` is therefore stored on the jet as
``pfParticleTransformerAK8MDJetTags:<flav>`` -- exactly the string NanoTuples used in
``bDiscriminator('pfParticleTransformerAK8MDJetTags:probHbb')``.

The tag infos and the ONNX scores are computed on ``updater.jetSource`` (the same jets the
updater iterates over), which is required because PATJetUpdater looks the scores up by jet Ref.
"""
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var
from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask, addToProcessAndTask
from PhysicsTools.PatAlgos.tools.jetTools import setupPuppiForPackedPF

from PhysicsTools.NanoTuples.pfParticleTransformerAK8_cff import (
    pfParticleTransformerAK8TagInfos,
    pfParticleTransformerAK8MDJetTags,
    _pfParticleTransformerAK8JetTagsAll,
)

# The only tagger that exists in NanoTuples; keep the dict shape of the original code.
CUSTOM_TAGGERS = {
    'InclParticleTransformerV2': {
        'nano_branch_name': 'ParT',
        'models': {  # jet radius -> (preprocess json, onnx model)
            0.8: ('PhysicsTools/NanoTuples/data/InclParticleTransformer-MD/ak8/V02/preprocess_corr.json',
                  'PhysicsTools/NanoTuples/data/InclParticleTransformer-MD/ak8/V02/model.onnx'),
            1.5: ('PhysicsTools/NanoTuples/data/InclParticleTransformer-MD/ak15/V02/preprocess_corr.json',
                  'PhysicsTools/NanoTuples/data/InclParticleTransformer-MD/ak15/V02/model.onnx'),
        },
    },
}


def _stored_discriminators():
    """Outputs that are written to NanoAOD (NanoTuples skipped the probHW* / probHZ* groups)."""
    return [d for d in _pfParticleTransformerAK8JetTagsAll if 'probHW' not in d and 'probHZ' not in d]


def getParTv2Branches(name='InclParticleTransformerV2'):
    """[(nano branch name, Var), ...] -- same names/doc/precision as NanoTuples ('ParT_<flav>')."""
    prefix = CUSTOM_TAGGERS[name]['nano_branch_name']
    return [(prefix + '_' + prob.split(':')[1],
             Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))
            for prob in _stored_discriminators()]


def addParTv2Tagger(process, updater, jetRadius, name='InclParticleTransformerV2', suffix=None,
                    pvSource='offlineSlimmedPrimaryVertices',
                    svSource='slimmedSecondaryVertices',
                    pfCandidates='packedPFCandidates',
                    lostTracks='lostTracks'):
    """Run ParTv2 on the jets of ``process.<updater>`` and store the scores in that updater.

    updater : label of a PATJetUpdater already in the process, e.g. 'updatedPatJetsAK15ParticleNet'
    """
    cfg = CUSTOM_TAGGERS[name]
    if jetRadius not in cfg['models']:
        raise ValueError('No %s model for jet radius %s' % (name, jetRadius))
    preprocess_json, model_path = cfg['models'][jetRadius]
    suffix = suffix if suffix is not None else 'R%d' % int(round(jetRadius * 10))

    task = getPatAlgosToolsTask(process)
    upd = getattr(process, updater)
    jets = upd.jetSource.value()
    puppi_value_map = setupPuppiForPackedPF(process)[0]

    tagInfosLabel = 'pfParticleTransformerAK8TagInfos' + suffix
    addToProcessAndTask(
        tagInfosLabel,
        pfParticleTransformerAK8TagInfos.clone(
            jets=jets,
            vertices=pvSource,
            secondary_vertices=svSource,
            pf_candidates=pfCandidates,
            lost_tracks=lostTracks,
            puppi_value_map=puppi_value_map,
            vertex_associator='',  # packedPFCandidates: PV association is read from the candidates
            jet_radius=jetRadius,
        ),
        process, task)

    # label must contain 'JetTags' followed by the suffix (see module docstring)
    tagsLabel = 'pfParticleTransformerAK8MDJetTags' + suffix
    addToProcessAndTask(
        tagsLabel,
        pfParticleTransformerAK8MDJetTags.clone(
            src=tagInfosLabel,
            preprocess_json=preprocess_json,
            model_path=model_path,
        ),
        process, task)

    # embed the scores into the PAT jets
    upd.addBTagInfo = cms.bool(True)
    sources = [cms.InputTag(tagsLabel, prob.split(':')[1]) for prob in _stored_discriminators()]
    existing = list(getattr(upd, 'discriminatorSources', cms.VInputTag()))
    upd.discriminatorSources = cms.VInputTag(*(existing + sources))
    return tagsLabel
