import os,sys
import pyqtgraph

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
from channelmap import getChannelMap

from collections import OrderedDict

class VireViewer( gl.GLViewWidget ):
    def __init__(self):
        super( VireViewer, self ).__init__()

        self.xmax = 10370.0
        self.ymax = 2330.0
        self.u_wires,self.v_wires,self.y_wires = self._define_wires()
        self.wires = [ self.u_wires,self.v_wires,self.y_wires ]
        self.chmap = getChannelMap()

        self.setCameraPosition(distance=16000)

        # offsetting u,y
        self.yoffsets = [ -2500, 0.0, 2500 ]
        self.zoffsets = [  -1, 0.0, 1 ]

        # expanding wire positions
        for wires,offset in zip(self.wires,self.yoffsets):
            wires[:,1] += offset
        #self.u_wires[:,1] -= 2500.0
        #self.y_wires[:,1] += 2500.0

        self.colors = [ np.ones( (self.u_wires.shape[0],4) ),
                        np.ones( (self.v_wires.shape[0],4) ),
                        np.ones( (self.y_wires.shape[0],4) ) ]
        for c in self.colors:
            c[:,3] = 0.1
        
        gl_u_wires = gl.GLLinePlotItem(pos=self.u_wires, color=self.colors[0], width=1.0, antialias=True, mode='lines')
        self.addItem( gl_u_wires )

        gl_v_wires = gl.GLLinePlotItem(pos=self.v_wires, color=self.colors[1], width=1.0, antialias=True, mode='lines')
        self.addItem( gl_v_wires )

        gl_y_wires = gl.GLLinePlotItem(pos=self.y_wires, color=self.colors[2], width=1.0, antialias=True, mode='lines')
        self.addItem( gl_y_wires )
        self.planes = [ gl_u_wires, gl_v_wires, gl_y_wires ]
        gl_v_wires.rotate(180,0,0,1)

        self.orbit( -135, 60 )
        self.collapsed = False # wires collapsed on top of on another

    def _getplanewire( self, crate, slot, femch ):
        if (crate,slot,femch) in self.chmap:
            return self.chmap[(crate,slot,femch)]
        else:
            return None

    def _define_wires(self, ):
        """define wire objects for drawing.
        
        the planes are:
          y=233
          z=1037

        we define verticle wires along y+, rotate by 60, then determine intersection of segment in frame?
        """
        
        # 'U' plane
        ymax = 2330.0  # mm
        xmax = 10370.0 # mm

        pitch = 3 # mm
        angle = 30 # horizontal
        slope = np.tan( -angle*np.pi/180.0 )
        xstep = pitch/np.sin( angle*np.pi/180.0 )
        validwire = True
        x = 7.9
        iwire = 0
        u_endpoints = []
        while validwire and iwire<2400:
            b = -slope*x # y-intercept
            x_at_ytop = (ymax - b)/slope
            y_at_xend = slope*(xmax) + b

            if b<ymax:
                pos2 = [0,b,0]
                if x<xmax:
                    pos1 = [x,0,0]
                else:
                    pos1 = [ xmax, y_at_xend,0.0 ]
            elif b>=ymax and x_at_ytop<xmax:
                pos2 = [ x_at_ytop,ymax,0.0 ]
                if x<xmax:
                    pos1 = [ x,0.0,0.0 ]
                else:
                    pos1 = [ xmax, y_at_xend,0.0 ]

            if pos1[0]>xmax+1 or pos1[1]>ymax+1:
                validwire = False
            if pos2[0]>xmax+1 or pos2[1]>ymax+1:
                validwire = False
                
            if validwire:
                #u_wires_np[iwire*2,:] = pos1[:]
                #u_wires_np[iwire*2+1,:] = pos2[:]
                u_endpoints.append( pos1 )
                u_endpoints.append( pos2 )
                #print iwire,pos1,pos2,xstep
            else:
                break                
            iwire += 1
            x += xstep
        print "Number of U-wires: ",iwire
        u_wires_np = np.array( u_endpoints )
        u_wires_np[:,0] -= xmax/2
        u_wires_np[:,1] -= ymax/2

        # reflecting U to get V
        v_wires_np = np.zeros( u_wires_np.shape )
        v_wires_np[:,0] = -u_wires_np[:,0]
        v_wires_np[:,1] = u_wires_np[:,1]

        # getting Y
        y_wires_np = np.zeros( (2*3456, 3) )
        for i in xrange(0,3456):
            y_wires_np[2*i,0] = -xmax/2 + i*3.0
            y_wires_np[2*i,1] = -ymax/2

            y_wires_np[2*i+1,0] = -xmax/2 + i*3.0
            y_wires_np[2*i+1,1] = ymax/2

        return u_wires_np,v_wires_np,y_wires_np

    def setWireColor( self, plane, wireid, color=np.array( (1.0,0.0,0.0,1.0) ) ):
        if type(color)==list or type(color)==tuple:
            if len(color)!=4:
                print "invalid color"
                return
            npcolor = np.array( color )
        elif isinstance(color,np.ndarray):
            npcolor = color

        if type(plane)==str:
            planeid = self.translatePlaneNameToID( plane )
        else:
            planeid = plane
        self.colors[planeid][2*wireid,:] = npcolor[:]
        self.colors[planeid][2*wireid+1,:] = npcolor[:]
        self.planes[planeid].setData( color=self.colors[planeid] )

    def setWireColorByCSF( self, crate, slot, femch, color=np.array( (1.0,0.0,0.0,1.0) ) ):
        planewire = self._getplanewire( crate, slot, femch )
        if planewire is None:
            print "Missing ",crate, slot, femch," in database. Ask Andrzej"
            return
        self.setWireColor( planewire[0], planewire[1], color=color )

    def setWires( self, wireid_tuple, color=np.array( (1.0,0.0,0.0,1.0) ) ):
        """activates a list of channels, supplied as a list of 2-tuple (plane,wireid)"""
        if type(wireid_tuple)!=tuple and type(wireid_tuple)!=list:
            print "invalid argument for wireid_tuple. need to supply tuple or list"
        for item in wireid_tuple:
            if len(item)!=2:
                print "invalid format, item in channel list must be (int plane,int wireid) or (str plane, int wireid)"
            self.setWireColor( item[0], item[1], color=color )

    def translatePlaneNameToID( self, name ):
        if name.upper()=='U':
            return 0
        elif name.upper()=='V':
            return 1
        elif name.upper()=='Y':
            return 2
        raise ValueError('unrecognized plane name: '+name)
        
    def resetWireColors( self ):
        for c in self.colors:
            c[:,:] = np.ones( 4 )[:]
            c[:,3] = 0.01

    def mouseMoveEvent(self, ev):
        diff = ev.pos() - self.mousePos
        self.mousePos = ev.pos()
        
        if ev.buttons() == QtCore.Qt.LeftButton:
            if (ev.modifiers() & QtCore.Qt.ControlModifier):
                self.orbit(-diff.x(), diff.y())
            else:
                self.pan(-10*diff.x(), 10.0*diff.y(), 0, relative=False)

    def paintGL(self, *args, **kwds):
        gl.GLViewWidget.paintGL(self, *args, **kwds)
        self.qglColor(QtCore.Qt.white)
        nfts = 11
        step = 12000.0/float(nfts-1)
        for ft in xrange(0,nfts):
            self.renderText(-6000+ft*step, 4000, 0, 'FT%d'%(ft+1))

    def collapseWires(self):
        if self.collapsed:
            return

        for wires,yoffset,zoffset in zip(self.wires,self.yoffsets,self.zoffsets):
            wires[:,1] -= yoffset
            wires[:,2] += zoffset
        self.collapsed = True

        for wires,plane in zip(self.wires,self.planes):
            plane.setData( pos=wires )

    def expandWires(self):
        if not self.collapsed:
            return

        for wires,yoffset,zoffset in zip(self.wires,self.yoffsets,self.zoffsets):
            wires[:,1] += yoffset
            wires[:,2] -= zoffset
        self.collapsed = False

        for wires,plane in zip(self.wires,self.planes):
            plane.setData( pos=wires )

    def save(self,fout):
        if type(fout)!=str:
            print "need string: ",fout
        if fout[-4:]==".png":
            self.readQImage().save(fout)
        else:
            self.readQImage().save(fout+".png")

class mainwindow( QtGui.QMainWindow ):
    def __init__(self):
        super( mainwindow, self ).__init__()
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        self.resize(1000,500)
        self.layout = QtGui.QHBoxLayout()
        self.cw.setLayout( self.layout )
        
        self.vires = VireViewer()
        #self.layout.addWidget( self.vires )

        # add form
#         self.colorWidget = QtGui.QWidget()
#         self.colorLayout = QtGui.QHBoxLayout()
#         self.colorCrate = QtGui.QLineEdit("1")
#         self.colorSlot = QtGui.QLineEdit("1")
#         self.colorChannel = QtGui.QLineEdit("1")
#         self.colorR = QtGui.QLineEdit("1")
#         self.colorG = QtGui.QLineEdit("1")
#         self.colorB = QtGui.QLineEdit("1")
#         self.colorR = QtGui.QLineEdit("1")
        
app = QtGui.QApplication([])
mw = mainwindow()
print "mw.vires is VireViewer class"
print "mw.vires.setWireColor( self, plane, wireid, color )"
print "mw.vires.show()"

def getmw():
    global mw
    return mw

if __name__ == "__main__":

    mw.vires.show()    
    #for i in xrange(0,1):
    #    mw.vires.setWireColor( 1, i+1000, np.array((1.0,0.0,0.0,1.0)) )

    #if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
    #    pg.QtGui.QApplication.exec_()
