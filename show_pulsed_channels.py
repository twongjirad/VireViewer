import os,sys
import numpy as np
import pandas as pd

def get_pulsed_channels():
    pulsed = pd.read_csv( open('pulsedChannel3.txt'), delimiter='\t' )
    print "Number of pulsed channels: ",len(pulsed)
    return pulsed.values
    
def show(mw,offset=0):
    pulsed = get_pulsed_channels()
    if mw is None:
        return
    for r in pulsed:
        print r
        mw.vires.setWireColor( r[0], r[1], (0.0, 0.0, 1.0, 1.0 ) )

    mw.vires.setWireColor( 'U', 1777, (0,1,0,1) )
    mw.vires.setWireColor( 'U', 1729, (0,1,0,1) )
    mw.vires.setWireColor( 'U', 2097, (0,1,0,1) )
    mw.vires.setWireColor( 'U', 2029, (0,1,0,1) )
    mw.vires.setWireColor( 'V',  207, (0,1,0,1) )
    for y in xrange(3233,3456,32):
        mw.vires.setWireColor( 'Y',y, (0,0,1,1) )


if __name__ == "__main__":
    show(None)
