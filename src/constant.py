import numpy as np

class SKINCONSTS(object):

	# define threshold constants for skin detection

	HSV_LOWER = np.array([0, 0, 120], dtype = np.uint8)
	HSV_UPPER = np.array([80, 255, 255], dtype = np.uint8)
	RGB_LOWER = np.array([45, 52, 108], dtype = np.uint8)
	RGB_UPPER = np.array([255, 255, 255], dtype = np.uint8)
	YCRCB_LOWER = np.array([90, 100, 130], dtype = np.uint8)
	YCRCB_UPPER = np.array([230, 120, 180], dtype = np.uint8)
	
	BINARY_THRESH = 60
	BLUR_CONST = 41 # Gaussian blur parameter