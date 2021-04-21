#!/usr/bin/env ccs-script
import os
import time
#import config
import sys
#sys.path.insert(0,"/home/homer/scripts/")
from pd import PhotodiodeReadout
#from org.lsst.ccs.utilities.location import LocationSet
#import jarray
from java.lang import String
from org.lsst.ccs.scripting import CCS
#from ccs import aliases
#from ccs import proxies
from java.time import Duration
#bb = CCS.attachProxy("ts8-bench")
bb = CCS.attachSubsystem("ts8-bench")
reb0 = CCS.attachSubsystem("ts8-fp/R22/Reb0")



def test_pd(exposure):
    pd_readout = PhotodiodeReadout(exposure)
    pd_readout.start_accumulation()
    time.sleep(2.5)
    print("starting exposure")

    reb0.sendSynchCommand("setRegister 0x100000 [0x103bc]")  # light
    time.sleep(exposure)
    reb0.sendSynchCommand("setRegister 0x100000 [0x3bc]")  # light

    print("exposure complete")

    time.sleep(5)

    print("buffer time complete")

    pd_readout.write_readings("/scratch/","pd-test-%s" % str(int(time.time())))

    return ()


# confirm that the reb and sequencer are in the expected state
resp = str(reb0.sendSynchCommand("getRegister 0x100000 1"))
rebstat = int(resp.split()[1],16)  # status
print "rebstat = %x" % rebstat
if rebstat!=0x3bc :
    print "Expecting rebstat = 0x3bc and it isn't! Aborting!"
    exit

#for i in range(2):
#    test_pd(0.5)
#for i in range(2):
#    test_pd(1)
##    time.sleep(2)
#for i in range(2):
#    test_pd(30)
for i in range(2):
    test_pd(50)
#for i in range(2):
#    test_pd(150)

#                self.take_image(exposure, expose_command, symlink_image_type='%s_%s_%s_flat%d' % (nd_filter, self.wl_filter, e_per_pixel, pair))
