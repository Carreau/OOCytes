#!python
# coding: utf-8
# run with the following stupid python if problems : 
#   ~/anaconda/python.app/Contents/MacOS/python
# 

import os
os.environ['ETS_TOOLKIT'] = 'qt4'
# By default, the PySide binding will be used. If you want the PyQt bindings
# to be used, you need to set the QT_API environment variable to 'pyqt'
#os.environ['QT_API'] = 'pyqt'

# To be able to use PySide or PyQt4 and not run in conflicts with traits,
# we need to import QtGui and QtCore from pyface.qt
from pyface.qt import QtGui, QtCore


import json
import skimage
import skimage.io
import oolib
import sys
import pandas
import matplotlib.pyplot as plt
import os.path as path
import io
import os.path
import numpy as np


    #fname=None


def main(fname):
    im = skimage.io.imread(fname,plugin='tifffile')
    nacc = oolib.timecorr3(im, im.shape[0])

    nsample = len(nacc)
    dt = 1
    time_a = np.arange(0,nsample)*dt
    (tau, offset),_ = oolib.fit_decay(time_a, nacc)

    df = pandas.DataFrame(nacc, columns=['correlation'])
    df['time'] = time_a
    print offset, tau
    df['fit'] = offset+np.exp(-time_a/tau)*(1-offset)
    df['tau'] = tau
    df['offset'] = offset
    df['halflife'] = tau*np.log(2)


    plt.plot(df.time,df.correlation, label='data')
    plt.plot(df.time, df.fit, '--',  label='fit')
    plt.title(os.path.basename(fname))
    plt.xlabel('time (s)')
    plt.ylabel('correlation')
    plt.legend()
    base_save =  path.join(
            path.dirname(fname),'roi-'+path.basename(fname)
        )


    plt.savefig(base_save+'.eps')

    df.to_csv(base_save+'.csv')
    df.to_excel(base_save+'.xls')
 
if __name__ == '__main__':
    
    if len(sys.argv)<2:
    	app = QtGui.QApplication(['myapp'])
    	fname = str(QtGui.QFileDialog.getOpenFileName())
    else :
        fname = sys.argv[1]

    main(fname)