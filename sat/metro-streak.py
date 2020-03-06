#!/usr/bin/env ccs-script                                                                                                           
from optparse import OptionParser
from org.lsst.ccs.scripting import CCS
from java.time import Duration

import time
                

# setup controls
    
ts = CCS.attachSubsystem("metrology/Positioner")
bb = CCS.attachSubsystem("ts8-raft")


tm = int(time.time())

# set output directory

output_dir = "/gpfs/slac/lsst/fs3/g/data/jobHarness/jh_stage/LCA-11021_RTM/LCA-11021_RTM-016/post_streakTest1_chk/%d/S${sensorLoc}/" % tm
bb.sendSynchCommand("setDefaultImageDirectory",output_dir)
print("The output directory has been set to - \n"+output_dir)

Timeout = Duration.ofSeconds(600)
CCS.setDefaultTimeout(Timeout)

start = time.time()

# starting point
xstart = 65.0
ystart = -72.6;
x = xstart
y = ystart
# step increments
dx = -10.0
dy = 10.0

ts.sendSynchCommand("moveAbs_xy",x,y)

# clear the sensors before starting
for iimg in range(10) :
    bb.sendSynchCommand("exposeAcquireAndSave",0,False,False,"")

print("time                   delta_t     X_measured  Y_measured")
for i in range(10) :

# move to new position

    print "%f %11.3f %11.3f %11.3f" % (time.time(),(time.time()-start),ts.sendSynchCommand("getPosX"),ts.sendSynchCommand("getPosY"))
    ts.sendSynchCommand("moveAbs_xy",x,y)
    x += dx
    y += dy

# optional extra clearing before each set of exposures
    for iimg in range(0) :
        bb.sendSynchCommand("exposeAcquireAndSave",0,False,False,"")

    for expt in [100] :

# acquire image

        for iimg in range(0) :
            bb.sendSynchCommand("exposeAcquireAndSave",expt,False,False,"S${sensorLoc}_streakTest_%dms_x_%06.2f_y_%06.2f_%d.fits" % (expt,x,y,iimg))
#
    time.sleep(0.2)

# take an image at the end

for expt in [100] :

    for iimg in range(1) :
        bb.sendSynchCommand("exposeAcquireAndSave",expt,False,False,"S${sensorLoc}_streakTest_%dms_x_%06.2f_y_%06.2f_final_%d.fits" % (expt,x,y,iimg))

# clear the sensors before starting return to start
for iimg in range(3) :
    bb.sendSynchCommand("exposeAcquireAndSave",0,False,False,"")

ts.sendSynchCommand("moveAbs_xy",xstart,ystart)

for expt in [2000] :

    for iimg in range(2) :
        bb.sendSynchCommand("exposeAcquireAndSave",expt,False,False,"S${sensorLoc}_streakTest_%dms_x_%06.2f_y_%06.2f_startreturn_%d.fits" % (expt,x,y,iimg))
