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

output_dir = "/gpfs/slac/lsst/fs3/g/data/jobHarness/jh_stage/LCA-11021_RTM/LCA-11021_RTM-004/mp_slit_intensitytester/%d/S${sensorLoc}/" % tm
bb.sendSynchCommand("setDefaultImageDirectory",output_dir)
print("The output directory has been set to - \n"+output_dir)

Timeout = Duration.ofSeconds(300)
CCS.setDefaultTimeout(Timeout)

start = time.time()


# reference values
#xstart = 310.0
#ystart = 210.0
#xend = 440.0
#yend = 300.0

# setup x scan
xstart = 280.0
xend = 340.0

# setup y scan
ystart = 240.
yend = 300.0

# setup z scan ... if any

#zstart = 35.5
#zend = 75.5
#zstart = 38
#zend = 46
zstart = 42
zend = 42

speed = 10.0

dz = 0.0

#nsteps = abs((zstart - zend) / abs(dz)) + 1
nsteps = 3

print('nsteps = '+str(nsteps))

#expt = 5000

# ---------------- x streak -------------------
ts.sendSynchCommand("moveTo","x",xstart,speed)
ts.sendSynchCommand("moveTo","y",ystart,speed)
ts.sendSynchCommand("moveTo","z",zstart,speed)

time.sleep(5.0)


# clear the sensors before starting
for iimg in range(5) :
    bb.sendSynchCommand("exposeAcquireAndSave",0,False,False,"")
    time.sleep(1)
# take some bias images
for iimg in range(5) :
    bb.sendSynchCommand("exposeAcquireAndSave",0,False,False,"S${sensorLoc}_bias_%d.fits" % iimg)
    time.sleep(1)

x = xstart
z = zstart

dx = (xend-xstart)/float(nsteps)
dy = (yend-ystart)/float(nsteps)


toggle = 0

nexp = 10


#while(z > (zstart-0.01) and z < (zend+0.01)) :
for ii in range(nsteps) :

    if (ii>0) :
        nexp = 1

    y = ystart

    while(y>=min(ystart,yend) and y<=max(ystart,yend)) :

        print('moving to : x = '+str(x)+', y = '+str(y)+', z = '+str(z))
#    if (toggle == 0) :
#        reb0.sendSynchCommand("setRegister 0x100000 [0x103d4]")  # light
#    if (toggle == 1) :
#        # light
#        reb0.sendSynchCommand("setRegister 0x100000 [0x3d4]")    # dark
#    toggle = (toggle + 1) % 2
        ts.sendSynchCommand("moveTo","z",z,speed)
        ts.sendSynchCommand("moveTo","x",x,speed)
        ts.sendSynchCommand("moveTo","y",y,speed)

        time.sleep(2.0)

        #    for expt in range(1000,10000,1000) :
        for target in [1,5,10, 20, 40, 80, 100, 125, 150, 200] :

#            expt = target * 25
            expt = target * 100

            for iexp in range(nexp) :

                print('starting exposure with expt = %d , index = %d' % (expt,iexp))
                # acquire image
                bb.sendSynchCommand("exposeAcquireAndSave",expt,True,False,"S${sensorLoc}_slit_xyz=%06.2f_%06.2f_%06.2fmm-sig=%06dK-exp=%05dms_%d.fits" % (x,y,z,target,expt,iexp))

                print("time before wait = %f" % time.time())
                bb.sendSynchCommand("waitForImage 10000")
                print("time after wait = %f" % time.time())

                time.sleep(1.0)

                for iimg in range(3) :
                    print("clearing image #%d"%iimg)
                    bb.sendSynchCommand("exposeAcquireAndSave",0,False,False,"")
                    print("bias: time before wait = %f" % time.time())
                    bb.sendSynchCommand("waitForImage 10000")
                    print("bias: time after wait = %f" % time.time())
                    time.sleep(2.0)
        y += dy

    x += dx
    z += dz




print('DONE')
