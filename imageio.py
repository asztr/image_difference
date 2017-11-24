#Library for exr manipulation. Reads and writes from exr 3-channel files to numpy (x,y,c) arrays.

#The natural representation of exrs is an array of 1D arrays each containing a channel (c, x*y).
#To transform to the other representation I'm using np.swapaxes and rgb2rgbdict.

import OpenEXR
import Imath
import numpy as np
import sys
from scipy import misc

#numpy array(x,y,c) to tuple of string rgb channels (input expected by OpenEXR writePixels)
def rgb2rgbdict(rgb):
	return { c:rgb[:,:,idx].ravel().tostring() for idx,c in enumerate("RGB") }

#reads EXR file to numpy array(y,x,c)
def readEXR(filenameEXR):
	pt = Imath.PixelType(Imath.PixelType.FLOAT) #only works hard-coding this and np.float32, instead of using the value from: exr.header()['channels'][c].type
	exr = OpenEXR.InputFile(filenameEXR)
	dw = exr.header()['dataWindow']
	size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
	#this needs to be fixed. 2 of the following 3 lines swap axes.
	rgb = np.swapaxes(np.array([np.fromstring(exr.channel(c, pt), dtype=np.float32) for c in "RGB"]), 0, 1) #I guess if we used HALF we would need to use np.float16
	rgb.shape = (size[1], size[0], 3) #numpy array are (row, col) = (y, x)
	rgb = np.swapaxes(rgb, 0, 1) #(y,x,c) -> (x,y,c) #probably (x,y,c) -> (y,x,c)
	exr.close()
	return rgb

#writes numpy array(y,x,c) to EXR file
def writeEXR(rgb, filenameEXR):
	size = rgb.shape
	header = OpenEXR.Header(size[0], size[1])
	rgbYX = np.swapaxes(rgb, 0, 1) #(y,x,c) -> (x,y,c)
	header['channels'] = { c:Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT)) for c in "RGB"} #shouldn't we check the type of rgb's elements?
	exr = OpenEXR.OutputFile(filenameEXR, header)
	exr.writePixels(rgb2rgbdict(rgbYX))
	exr.close()

#for file reading
def gamma_decode(rgb, gamma=2.2, maxval=255.0):
	return (rgb/maxval)**gamma

#for file writing
def gamma_encode(rgb, gamma=2.2, maxval=255.0):
	return maxval*(rgb**(1.0/gamma))

def read_image(filename):
	ext = filename.split('.')[-1]

	if (ext.lower() == 'exr'):
		rgb = readEXR(filename)
		rgb = np.swapaxes(rgb, 0, 1)
	else:
		rgb = misc.imread(filename)
		rgb = gamma_decode(rgb, gamma=2.2, maxval=255.0)
	return rgb

def write_image(rgb, filename):
	ext = filename.split('.')[-1]

	if (ext.lower() == 'exr'):
		rgb = np.swapaxes(rgb, 0, 1)
		writeEXR(rgb, filename)
	else:
		rgb = gamma_encode(rgb, gamma=2.2, maxval=255.0)
		rgb = misc.imsave(filename)
