import os,sys
import pandas as pd
import numpy as np

def get_badchtable():
    f = open('bad_channel_table.txt')
    badch = pd.read_csv( open('bad_channel_table.txt') )
    return badch

def get_index( crate, slot, femch ):
    index = crate*64*15 + (slot-4)*64 + femch
    return index

def get_badchtable_whistidx():
    badch = get_badchtable()
    badch['hist_id'] = np.vectorize( get_index )( badch['Crate'], badch['Slot'], badch['FEM Channel'] )
    return badch

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def showallbadch(mw):
    badch = get_badchtable()
    for r in badch.to_records():
        print "setting badch: ",r['Wire Plane'], r['Wire Number']
        mw.vires.setWireColor( r['Wire Plane'], r['Wire Number'] )

def showbadch(mw,df):
    for r in df.to_records():
        print "setting badch: ",r['Wire Plane'], r['Wire Number']
        mw.vires.setWireColor( r['Wire Plane'], r['Wire Number'] )

if __name__ == "__main__":
    badch = get_badchtable()
    badch['hist_id'] = np.vectorize( get_index )( badch['Crate'], badch['Slot'], badch['FEM Channel'] )
    print_full(badch)

