#!/bin/bash
# Reformat benchmark data files so that they are consistent with all the other
# models
# 1) Extract variables by model
# 2) Rename variables by stripping the model name from the variable name

models="1lin 2lin 3km27"
vars="Qle Qh NEE Rnet"
basedir="/Users/nijssen/Dropbox/data/PLUMBER/PLUMBER_data/benchmark_data"

cwd=`pwd`
cd ${basedir}
for model in ${models}
do
  mkdir -p ${model}
  extractstr='-v'
  renamestr=''
  for var in ${vars}
  do
    extractstr=${extractstr}"${var}_${model},"
    renamestr=${renamestr}" -v${var}_${model},${var}"
  done
  extractstr=${extractstr%,}
  for file in *_1.4_PLUMBER_benchmarks.nc
  do
    site=${file%Fluxnet_1.4_PLUMBER_benchmarks.nc}
    outfile=${model}/${model}_${site}Fluxnet.1.4.nc
    ncks ${extractstr} ${file} ${outfile}
    ncrename -O ${renamestr} ${outfile}
  done
done
cd ${cwd}
