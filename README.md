# VireViewer

##Dependencies

* Qt4
* PyQt or PySide
* pyqtgraph
* numpy
* optional: ipython (for interactivity)

##Showing bad channels (ipython)

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