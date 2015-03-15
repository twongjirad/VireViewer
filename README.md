# VireViewer

##Dependencies

* Qt4 (GUI backend)
* PyQt or PySide (python bindings)
* pyqtgraph (python module for drawing)
* numpy
* optional: ipython (for interactivity)


##Load tool
```
ipython
In [1]: run vireviewer.py
mw.vires is VireViewer class
mw.vires.setWireColor( self, plane, wireid, color )
mw.vires.show()
```

mw is a Qt MainWindow widget. mw.vires is a Widget for the window drawing the wires. 

## Set Wire Color

To set a wire to a color, the latter specified by a RGBA value. For example to set wire
1234 on the U plane to blue do

```
In [2]: mw.vires.setWireColor( 'U', 1234, (0.0,0.0,1.0,1.0) )
```

Then to reset all the wires back to white, do
```
In [3]:	mw.vires.resetWireColors()
```

##Showing bad channels

```
ipython
In [1]: run vireviewer.py
mw.vires is VireViewer class
mw.vires.setWireColor( self, plane, wireid, color )
mw.vires.show()
In [2]: import show_bad_channels
In [3]: show_bad_channels.show(mw)
```

![alt tag](https://raw.github.com/twongjirad/VireViewer/master/screenshots/bad_channels.png)


##Collapse Wires on top of one another
```
(after above)
In [4]: mw.vires.collapseWires()
```

![alt tag](https://raw.github.com/twongjirad/VireViewer/master/screenshots/bad_channels_collapsed.png)

To reexpand them
```
(after above)
In [4]: mw.vires.expandWires()
```