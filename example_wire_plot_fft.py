import os,sys
sys.path.append("/Users/twongjirad/working/uboone/vireviewer")
from vireviewer import getmw
import numpy as np
import pandas as pd
from channelmap import getChannelMap
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

print "EXAMPLE ONLY. WON'T WORK"
sys.exit(-1)

def plot_run( mw, run, subrun1, subrun2, plotfft=True ):
    npzfile = np.load( 'output/run%03d_subrun%03d_%03d.npz'%(run,subrun1,subrun2) )
    arr = npzfile['wffftrgba']
    df = pd.DataFrame( arr )
    maxamp = df.query('(crate==%d) & (slot==%d) & (femch==%d)'%(6,9,0) )['max_amp'].values[0]
    print "maxamp: ",maxamp
    chmap = getChannelMap()
    for r in arr:
        row = chmap.query( '(crate==%d) & (slot==%d) & (femch==%d)'%(r['crate'],r['slot'],r['femch']) )
        if len(row)>0:
            wireid = row['wireid'].values[0]
            plane = row['plane'].values[0]
            # FFT
            if plotfft:
                red = r['rval']
                g = r['gval']
                b = r['bval']

                #if above_thresh:
                mw.vires.setWireColor( plane, wireid, ( 0.05+red, 0.05+g, 0.05+b, 1.0 ) )
                #else:
                #    mw.vires.setWireColor( plane, wireid, ( 1.0, 1.0, 1.0, 0.1 ) )
                print r['crate'],r['slot'],r['femch'],plane,wireid,red,g,b
                # pulsed wire color
                if (r['crate'],r['slot'],r['femch'])==(6,9,0):
                    mw.vires.setWireColor( plane, wireid, ( 1.0, 1.0, 1.0, 1.0 ) )
            # AMP
            else:
                if ( r['max_amp']>10.0 ):
                    mw.vires.setWireColor( plane, wireid, ( 0.1 + 0.9*r['max_amp']/maxamp, 0.0, 0.0, 1.0 ) )
                else:
                    mw.vires.setWireColor( plane, wireid, ( 1.0, 1.0, 1.0, 0.1 ) )
                print r['crate'],r['slot'],r['femch'],plane,wireid,r['max_amp']

                # pulsed wire color
                if (r['crate'],r['slot'],r['femch'])==(6,9,0):
                    mw.vires.setWireColor( plane, wireid, ( 0.0, 1.0, 0.0, 1.0 ) )


if __name__ == "__main__":
    mw = getmw()
    #plot_run( mw, 95, 44, 55 )
    #mw.show()
    #if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):                                                                                                                           
    pg.QtGui.QApplication.exec_()  
    raw_input()
