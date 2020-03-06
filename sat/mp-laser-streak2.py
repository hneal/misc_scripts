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

Timeout = Duration.ofSeconds(300)
CCS.setDefaultTimeout(Timeout)

start = time.time()

iset = 1

if iset==0 :
    xstart1 = 310.0
    ystart1 = 185.0
    xend1 = 420.0
    yend1 = 300.0
elif iset==1 : # y scan
    xstart1 = 310.0
    ystart1 = 150.0
    xend1 = 310.0
    yend1 = 300.0
elif iset==2 : # x scan
    xstart1 = 310.0
    ystart1 = 187.0
    xend1 = 420.0
    yend1 = 187.0
else :
    print('illegal iset = %d' % iset)
    exit

speed = 15.0

nsteps = 1


expt = 10000

# ---------------- x streak -------------------
ts.sendSynchCommand("moveTo","x",xstart1,speed)
ts.sendSynchCommand("moveTo","y",ystart1,speed)

time.sleep(5.0)


# clear the sensors before starting
for iimg in range(3) :
    bb.sendSynchCommand("exposeAcquireAndSave",0,False,False,"")


x = xstart1
y = ystart1
dx = (xend1-xstart1)/float(nsteps)
dy = (yend1-ystart1)/float(nsteps)


for istep in range(nsteps) :
    ts.sendSynchCommand("moveTo","x",x,speed)
    ts.sendSynchCommand("moveTo","y",y,speed)
    x += dx
    y += dy
    print('x = '+str(x)+', y = '+str(y))
ts.sendSynchCommand("moveTo","x",x,speed)
ts.sendSynchCommand("moveTo","y",y,speed)

print('starting exposure')
# acquire image
bb.sendSynchCommand("exposeAcquireAndSave",expt,True,False,"S${sensorLoc}_mp-laser-streak_xy1=%06.2f_%06.2f-xy2=%06.2f_%06.2f.fits" % (xstart1,ystart1,xend1,yend1))

print('DONE')

#


