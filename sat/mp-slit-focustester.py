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

output_dir = "/gpfs/slac/lsst/fs3/g/data/jobHarness/jh_stage/LCA-11021_RTM/LCA-11021_RTM-004/mp_slit_focustester/%d/S${sensorLoc}/" % tm
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
    xend1 = 310.0

    ystart1 = 280.0
    yend1 = 280.0

else :
# x scan - vertical on ds9 display
    xstart1 = 310.0
    xend1 = 310.0

    ystart1 = 280.0
    yend1 = 280.0



#zstart1 = 35.5
#zend1 = 75.5
#zstart1 = 38
#zend1 = 46
zstart1 = 1
zend1 = 9

speed = 10.0

dz = 1.0

nsteps = abs((zstart1 - zend1) / abs(dz)) + 1

print('nsteps = '+str(nsteps))

expt = 5000

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

while(z > (zstart1-0.01) and z < (zend1+0.01)) :
#    if (toggle == 0) :
#        reb0.sendSynchCommand("setRegister 0x100000 [0x103d4]")  # light
#    if (toggle == 1) :
#        # light
#        reb0.sendSynchCommand("setRegister 0x100000 [0x3d4]")    # dark

    toggle = (toggle + 1) % 2
    ts.sendSynchCommand("moveTo","z",z,speed)
    ts.sendSynchCommand("moveTo","x",x,speed)
    ts.sendSynchCommand("moveTo","y",y,speed)

    time.sleep(2.0)

    print('starting exposure')
# acquire image
    bb.sendSynchCommand("exposeAcquireAndSave",expt,True,False,"S${sensorLoc}_mp-laser-slit_z=%06.2f.fits" % (z))


    x += dx
    y += dy
    z += dz
    print('x = '+str(x)+', y = '+str(y)+', z = '+str(z))




print('DONE')
