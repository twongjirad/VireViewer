import os,sys
#import numpy as np
#import pandas as pd

channelmap = None

def getChannelMap():
    global channelmap
    if channelmap is None:
        print "Build Channel Map"
        channelmap = {}
        f = open('csf2planewire.txt','r')
        lines = f.readlines()
        #maparr = np.zeros( (len(lines[2:]),5), dtype=[ ('crate',int), ('slot',int), ('femch',int), ('plane','|S2'), ('wireid',int) ] )
        #maparr = np.zeros( (len(lines[2:])), dtype=[ ('crate','i4'), ('slot','i4'), ('femch','i4'), ('plane','|S2'), ('wireid','i4') ] )
        for n,l in enumerate(lines[2:]):
            l = l.strip().split("|")
            if l is None:
                continue
            crate = int(l[0].strip())
            slot  = int(l[1].strip())
            femch = int(l[2].strip())
            plane = l[3].strip()
            wireid = int(l[4].strip())
            #maparr[n]['crate'] = crate
            #maparr[n]['slot'] = slot
            #maparr[n]['femch'] = femch
            #maparr[n]['plane'] = plane
            #maparr[n]['wireid'] = wireid
            channelmap[ (crate,slot,femch) ] = ( plane, wireid )
    return channelmap

if __name__=="__main__":
    chmap = getChannelMap()
    chmap = getChannelMap()
    print chmap
    print type(chmap)
