#!/usr/bin/env ccs-script                                                                                                           
from optparse import OptionParser
from org.lsst.ccs.scripting import CCS
#from ccs import aliases
import time
                    
#from ccs import proxies
#fp = CCS.attachProxy("ts7-2/Cryo")
ts = CCS.attachSubsystem("ts7-2/Cryo")

start = time.time()
while(True):
    print "%f %11.3f %11.3f %11.3f %11.3f %11.3f" % (time.time(),(time.time()-start),ts.sendSynchCommand("getTemp A"),ts.sendSynchCommand("getTemp B"),ts.sendSynchCommand("getTemp C"),ts.sendSynchCommand("getTemp D"))
    time.sleep(5.0)
