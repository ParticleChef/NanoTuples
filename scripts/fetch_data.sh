#!/bin/bash
# Run from the package directory (PhysicsTools/NanoTuples). Pulls the ONNX models/preprocessing
# files (~83 MB, unchanged from NanoTuples) into ./data
set -e
TMP=$(mktemp -d)
git clone --depth 1 --branch dev/ParTv2/CMSSW_13_3_1_patch1 https://github.com/hqucms/NanoTuples.git "$TMP/nt"
rm -rf data && cp -r "$TMP/nt/data" ./data
rm -rf "$TMP"
find data -name md5sum.txt -execdir md5sum -c md5sum.txt \;
ls -R data | head -30
