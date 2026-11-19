#!/usr/bin/env python3
"""Sanity-check a NanoTuples-v15 output file: python3 checkBranches.py nano.root  (needs uproot)"""
import sys
import uproot

f = uproot.open(sys.argv[1])
t = f['Events']
keys = t.keys()

expect = {
    'AK15Puppi': ['pt', 'eta', 'phi', 'mass', 'area', 'rawFactor', 'tau1', 'tau2', 'tau3', 'msoftdrop',
                  'nBHadrons', 'nCHadrons', 'subJetIdx1', 'subJetIdx2'],
    'AK15PuppiSubJet': ['pt', 'eta', 'phi', 'mass', 'area', 'rawFactor'],
    'GenJetAK15': ['pt', 'eta', 'phi', 'mass'],        # MC only
    'GenSubJetAK15': ['pt', 'eta', 'phi', 'mass'],     # MC only
}
for coll, vars_ in expect.items():
    present = [v for v in vars_ if '%s_%s' % (coll, v) in keys]
    status = 'OK ' if len(present) == len(vars_) else ('-- ' if not present else 'BAD')
    print('%s %-18s %d/%d  (n%s: %s)' % (status, coll, len(present), len(vars_), coll, 'n' + coll in keys))

for prefix in ('AK15Puppi_ParticleNetMD_', 'AK15Puppi_ParT_', 'FatJet_ParT_'):
    n = sum(k.startswith(prefix) for k in keys)
    print('%-28s %d branches  (expected: ParticleNetMD 5, ParT 37)' % (prefix + '*', n))
print('FatJet_globalParT3_* (official v15):', sum(k.startswith('FatJet_globalParT3_') for k in keys))
if 'AK15Puppi_jetId' in keys:
    print('AK15Puppi_jetId present (addJetID=True)')
