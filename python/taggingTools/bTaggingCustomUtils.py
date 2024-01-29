def updateSupportedBtagDiscr(supportedBtagInfos, supportedBtagDiscr, supportedMetaDiscr):

    # Update taggers in InclParticleTransformerV2
    from PhysicsTools.NanoTuples.taggingTools.pfMassDecorrelatedInclParticleTransformerV2_cff import _pfMassDecorrelatedInclParticleTransformerV2JetTagsProbs, _pfMassDecorrelatedInclParticleTransformerV2JetTagsMetaDiscrs, _pfMassDecorrelatedInclParticleTransformerAK15V2JetTagsProbs, _pfMassDecorrelatedInclParticleTransformerAK15V2JetTagsMetaDiscrs

    # update supportedBtagDiscr
    supportedBtagInfos.extend(["pfMassDecorrelatedInclParticleTransformerV2TagInfos"])
    for disc in _pfMassDecorrelatedInclParticleTransformerV2JetTagsProbs + _pfMassDecorrelatedInclParticleTransformerV2JetTagsMetaDiscrs:
        supportedBtagDiscr[disc] = [["pfMassDecorrelatedInclParticleTransformerV2TagInfos"]]
    for disc in _pfMassDecorrelatedInclParticleTransformerAK15V2JetTagsProbs + _pfMassDecorrelatedInclParticleTransformerAK15V2JetTagsMetaDiscrs:
        supportedBtagDiscr[disc] = [["pfMassDecorrelatedInclParticleTransformerAK15V2TagInfos"]]
    # update supportedMetaDiscr
    for disc in _pfMassDecorrelatedInclParticleTransformerV2JetTagsMetaDiscrs:
        supportedMetaDiscr[disc] = _pfMassDecorrelatedInclParticleTransformerV2JetTagsProbs
    for disc in _pfMassDecorrelatedInclParticleTransformerAK15V2JetTagsMetaDiscrs:
        supportedMetaDiscr[disc] = _pfMassDecorrelatedInclParticleTransformerAK15V2JetTagsProbs

    return supportedBtagInfos, supportedBtagDiscr, supportedMetaDiscr


def updateBTagModule(mod):
    import PhysicsTools.NanoTuples.taggingTools.pfMassDecorrelatedInclParticleTransformerV2_cff as tags
    for obj in dir(tags):
        if obj.startswith("pf"):
            setattr(mod, obj, getattr(tags, obj))
