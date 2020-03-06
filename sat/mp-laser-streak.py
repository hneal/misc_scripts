#!/usr/bin/env ccs-script                                                                                                           
from optparse import OptionParser
from org.lsst.ccs.scripting import CCS
from java.time import Duration

import time
                

# setup controls
    
ts = CCS.attachSubsystem("ts8-motorplatform")
bb = CCS.attachSubsystem("ts8-raft")


tm = int(time.time())

# set output directory

output_dir = "/gpfs/slac/lsst/fs3/g/data/jobHarness/jh_stage/LCA-11021_RTM/LCA-11021_RTM-004/mp_laser_streak/%d/S${sensorLoc}/" % tm
bb.sendSynchCommand("setDefaultImageDirectory",output_dir)
print("The output directory has been set to - \n"+output_dir)

Timeout = Duration.ofSeconds(100)
CCS.setDefaultTimeout(Timeout)

start = time.time()


xstart1 = 310.0
ystart1 = 240.0
xend1 = 430.0
yend1 = 240.0

xstart2 = 370.0
ystart2 = 180.0
xend2 = 370.0
yend2 = 300.0

speed = 10.0

expt = 10000

# ---------------- x streak -------------------
ts.sendSynchCommand("moveTo","x",xstart1,speed)
ts.sendSynchCommand("moveTo","y",ystart1,speed)

time.sleep(3.0)


# clear the sensors before starting
for iimg in range(3) :
    bb.sendSynchCommand("exposeAcquireAndSave",0,False,False,"")


if (xend1 != xstart1):
    ts.sendSynchCommand("moveTo","x",xend1,speed)
if (yend1 != ystart1):
    ts.sendSynchCommand("moveTo","y",yend1,speed)
# acquire image
bb.sendSynchCommand("exposeAcquireAndSave",expt,True,False,"S${sensorLoc}_mp-laser-streak_%dms_x1_%06.2f_x2_%06.2f.fits" % (expt,xstart1,xend1))


#
time.sleep(3.0)


# ---------------- y streak -------------------
ts.sendSynchCommand("moveTo","x",xstart2,speed)
ts.sendSynchCommand("moveTo","y",ystart2,speed)

time.sleep(3.0)

# clear the sensors before starting
for iimg in range(3) :
    bb.sendSynchCommand("exposeAcquireAndSave",0,False,False,"")


if (xend2 != xstart2):
    ts.sendSynchCommand("moveTo","x",xend2,speed)
if (yend2 != ystart2):
    ts.sendSynchCommand("moveTo","y",yend2,speed)
# acquire image
    bb.sendSynchCommand("exposeAcquireAndSave",expt,True,False,"S${sensorLoc}_mp-laser-streak_%dms_y1_%06.2f_y2_%06.2f.fits" % (expt,ystart2,yend2))


