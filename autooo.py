#!/bin/env python
# coding: utf-8
import json
import skimage
import skimage.io
import oolib
import PyQt4.QtGui
import matplotlib.pyplot as plt
import os.path as path
import io
import numpy as np

app = PyQt4.QtGui.QApplication(['myapp'])
fname = str(PyQt4.QtGui.QFileDialog.getOpenFileName())

im = skimage.io.imread(fname,plugin='tifffile')
nacc = oolib.timecorr3(im, im.shape[0])
plt.plot(nacc)
plt.title(fname)
plt.xlabel('time (# of frame)')
plt.ylabel('correlation')
base_save =  path.join(
        path.dirname(fname),'roi-'+path.basename(fname)
    )
plt.savefig(base_save+'.eps')
#with io.open(base_save+'.json', 'w') as f:
#    json.dump(f,list(nacc))

#np.savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')
np.savetxt(base_save+'.csv', nacc)
