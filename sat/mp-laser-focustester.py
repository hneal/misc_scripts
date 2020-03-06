#!/usr/bin/env ccs-script                                                                                                           
from optparse import OptionParser
from org.lsst.ccs.scripting import CCS
from java.time import Duration

import time
                

# setup controls
    
ts = CCS.attachSubsystem("ts8-motorplatform")
bb = CCS.attachSubsystem("ts8-raft")
reb0 = CCS.attachSubsystem("ts8-raft/R00.Reb0")


tm = int(time.time())

# set output directory

output_dir = "/gpfs/slac/lsst/fs3/g/data/jobHarness/jh_stage/LCA-11021_RTM/LCA-11021_RTM-004/mp_laser_focustester/%d/S${sensorLoc}/" % tm
bb.sendSynchCommand("setDefaultImageDirectory",output_dir)
print("The output directory has been set to - \n"+output_dir)

Timeout = Duration.ofSeconds(300)
CCS.setDefaultTimeout(Timeout)

start = time.time()


# reference values
#xstart1 = 310.0
#ystart1 = 210.0
#xend1 = 440.0
#yend1 = 300.0

doyscan = False

if doyscan:
# y scan - horizontal on ds9 display
    xstart1 = 310.0
#xend1 = 420.0
    xend1 = 310.0

    ystart1 = 190.0
    yend1 = 280.0

else :
# x scan - vertical on ds9 display
    xstart1 = 310.0
    xend1 = 420.0

    ystart1 = 190.0
#yend1 = 280.0
    yend1 = 190.0



zstart1 = 75.75
zend1 = 65.0

speed = 15.0

dz = -0.75

nsteps = (zstart1 - zend1) / abs(dz)

print('nsteps = '+str(nsteps))

expt = 80000

# ---------------- x streak -------------------
ts.sendSynchCommand("moveTo","x",xstart1,speed)
ts.sendSynchCommand("moveTo","y",ystart1,speed)
ts.sendSynchCommand("moveTo","z",zstart1,speed)

time.sleep(5.0)


# clear the sensors before starting
for iimg in range(3) :
    bb.sendSynchCommand("exposeAcquireAndSave",0,False,False,"")


x = xstart1
y = ystart1
z = zstart1

dx = (xend1-xstart1)/float(nsteps)
dy = (yend1-ystart1)/float(nsteps)


toggle = 0

while(z < (zstart1+0.01) and z > (zend1+0.01)) :
#    if (toggle == 0) :
#        reb0.sendSynchCommand("setRegister 0x100000 [0x103d4]")  # light
#    if (toggle == 1) :
#        # light
#        reb0.sendSynchCommand("setRegister 0x100000 [0x3d4]")    # dark

    toggle = (toggle + 1) % 2
    ts.sendSynchCommand("moveTo","z",z,speed)
    ts.sendSynchCommand("moveTo","x",x,speed)
    ts.sendSynchCommand("moveTo","y",y,speed)
    x += dx
    y += dy
    z += dz
    print('x = '+str(x)+', y = '+str(y))

# make a little box at the end
ts.sendSynchCommand("moveTo","x",x+2,speed)
ts.sendSynchCommand("moveTo","y",y,speed)
ts.sendSynchCommand("moveTo","x",x+2,speed)
ts.sendSynchCommand("moveTo","y",y+2,speed)
ts.sendSynchCommand("moveTo","x",x,speed)
ts.sendSynchCommand("moveTo","y",y+2,speed)
ts.sendSynchCommand("moveTo","x",x,speed)
ts.sendSynchCommand("moveTo","y",y,speed)


print('starting exposure')
# acquire image
bb.sendSynchCommand("exposeAcquireAndSave",expt,True,False,"S${sensorLoc}_mp-laser-streak_xy1=%06.2f_%06.2f-xy2=%06.2f_%06.2f.fits" % (xstart1,ystart1,xend1,yend1))

print('DONE')
