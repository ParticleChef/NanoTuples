import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoTuples.ak15_cff import setupAK15
from PhysicsTools.NanoTuples.ak8_cff import addCustomTaggerAK8
from PhysicsTools.NanoTuples.pfcands_cff import addPFCands


def nanoTuples_customizeCommon(process, runOnMC, addAK15=True, addPFcands=False,
                               customAK8Taggers=['InclParticleTransformerV2'],
                               customAK15Taggers=['InclParticleTransformerV2'],
                               addJetID=False):
    pfcand_params = {'srcs': [], 'isPuppiJets': [], 'jetTables': []}
    if addAK15:
        setupAK15(process, runOnMC=runOnMC, runParticleNetMD=True, customAK15Taggers=customAK15Taggers,
                  addJetID=addJetID)
        pfcand_params['srcs'].append('ak15WithUserData')
        pfcand_params['isPuppiJets'].append(True)
        pfcand_params['jetTables'].append('ak15Table')
    if len(customAK8Taggers) > 0:
        addCustomTaggerAK8(process, customAK8Taggers)
        pfcand_params['srcs'].append('updatedJetsAK8WithUserData')
        pfcand_params['isPuppiJets'].append(True)
        pfcand_params['jetTables'].append('fatJetTable')
    if addPFcands:
        addPFCands(process, outTableName='PFCands', **pfcand_params)

    return process


def nanoTuples_customizeData(process):
    process = nanoTuples_customizeCommon(process, runOnMC=False)
    return process


def nanoTuples_customizeMC(process):
    process = nanoTuples_customizeCommon(process, runOnMC=True)
    return process
