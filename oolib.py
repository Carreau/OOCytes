"""
Lib for oocyte analysis

"""

import matplotlib
import numpy as np
from matplotlib.pylab import subplots
from numpy import *
from scipy.optimize import curve_fit


def func(x, b, c):
    return (1-c)*np.exp(-b*x) + c


def make_roi(im, roix, roiy, roiw, roih, color=None, plot=True, ax=None):
    if color is None:
        color = 'white'

    x,y= 0, 0
    w,h = shape(im)[2], shape(im)[1]
    xm,ym= x+w,y+h
    roi = im[:,roiy:roiy+roih,roix:roix+roiw]
    if plot:
        if ax is None:
            fig,(ax) = subplots(1,1)
            fig.set_figheight(5)
            fig.set_figwidth(6)
    #    xm,ym= 650,900
        ax.imshow(im[0,y:ym,x:xm], cmap='gray', extent=(x,xm, y, ym), origin='top')
        ax.grid()
        
        #roix,roiy = 500,600
        #roiw,roih = 100,100
        
    
        from matplotlib.patches import  Rectangle
        lw=4
        rects = [Rectangle(xy=[roix+lw, roiy+lw], width=roiw-2*lw, height=roih-2*lw, fill=False )]  # filled rectangle
        ax.add_artist(rects[0])
        rects[0].set_lw(2)
        rects[0].set_color(color)
    return roi

def imc( im1, im2 , mean1=None, std1=None):
    """ compute the correlation  between image 1 and 2 """
    if not mean1:
        mean1 = im1.mean()
    if not std1:
        std1 = im1.std()
    return ((im1-mean1)*(im2-im2.mean())).sum()/std1/im2.std()/np.prod(np.shape(im1))


def timecorr(imge, rnge, window):
    acc = []
    for t0 in range(rnge):
        cc = []
        for i in range(window):
            cc.append(imc(imge[t0],imge[t0+i]))
        acc.append(cc)
    return array(acc)

def timecorr2(imge, rnge, window):
    mean1 = imge[:rnge].mean()
    std1 = imge[:rnge].std()
    cc = zeros(window)
    for i in range(window):
        cc[i] = imc(imge[:rnge],imge[i:i+rnge], mean1=mean1, std1=std1)
    return cc

def timecorr3(imge, window):

    cc = ones(window)
    for i in range(window-1):
        # +1 because by deinititon
        # for i =0 we have 1 
        cc[i+1] = imc(imge[:-i-1],imge[i+1:])
    return cc


def fit_decay(time, correlation):
    """
    Fit the correlation as a function of time with an exponential decay
    
    params
        time: array
        correlation: array
        
    TODO: have the initial parameter setable, or autodetect
    
    retrun:
        (popt, pcov)
    """
    popt, pcov = curve_fit(func, time, correlation, p0=(1e-2,0.1))
    
    return (popt, pcov)
