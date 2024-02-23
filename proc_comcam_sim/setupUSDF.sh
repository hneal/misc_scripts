#!/bin/bash
# setup Rubin env
export LSST_VERSION=w_2024_08
#export LSST_VERSION=w_2023_24
#export LSST_VERSION=w_2022_48
#export LSST_VERSION=w_2022_41
#export LSST_VERSION=w_2022_39
source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/${LSST_VERSION}/loadLSST.bash 
setup lsst_distrib

#export LSST_VERSION=d_2022_09_20
#source /sdf/group/rubin/sw/d_latest/loadLSST.bash
#setup lsst_distrib -t ${LSST_VERSION}

# setup PanDA env. Will be a simple step when the deployment of PanDA is fully done.
export PANDA_CONFIG_ROOT=$HOME
export PANDA_URL_SSL=https://pandaserver-doma.cern.ch:25443/server/panda
export PANDA_URL=http://pandaserver-doma.cern.ch:25080/server/panda
export PANDAMON_URL=https://panda-doma.cern.ch
export PANDA_AUTH=oidc
export PANDA_VERIFY_HOST=off
export PANDA_AUTH_VO=Rubin

# IDDS_CONFIG path depends on the weekly version
export PANDA_SYS=$CONDA_PREFIX
export IDDS_CONFIG=${PANDA_SYS}/etc/idds/idds.cfg.client.template

# WMS plugin
export BPS_WMS_SERVICE_CLASS=lsst.ctrl.bps.panda.PanDAService

#export HTTP_PROXY=http://atlsquid.slac.stanford.edu:3128
#export HTTPS_PROXY=tthps:/eups.lsst.codes/stack/src
#export https_proxy=http://atlsquid.slac.stanford.edu:3128
#export http_proxy=http://atlsquid.slac.stanford.edu:3128
