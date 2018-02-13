import numpy as np
import cv2
from constant import SKINCONSTS

class skinDetector(object):

	def __init__(self):
		pass

	def hsv_mask(self, im, debug = False):
		assert isinstance(im, np.ndarray)
		assert im.ndim == 3




		hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, SKINCONSTS.HSV_LOWER, SKINCONSTS.HSV_UPPER)

		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
		mask = cv2.erode(mask, kernel, iterations = 2)
		mask = cv2.dilate(mask, kernel, iterations = 2)
		mask = cv2.GaussianBlur(mask, (3, 3), 0)

		skin = cv2.bitwise_and(im, im, mask = mask)

		if debug:
			#cv2.imshow("original", im)
			cv2.imshow("hsv", hsv)
			cv2.imshow("mask", mask)
			cv2.imshow("skin", skin)
			cv2.waitKey(0)

		return mask.astype(float)

	def rgb_mask(self, im, debug = False):
		assert isinstance(im, np.ndarray)
		assert im.ndim == 3


		rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
		a = cv2.inRange(rgb, SKINCONSTS.RGB_LOWER, SKINCONSTS.RGB_UPPER)
		b = 255*((rgb[ :, :, 2] - rgb[ :, :, 1]) / 20)
		c = 255*((np.max(rgb, axis = 2) - np.min(rgb, axis = 2)) / 20)
		d = np.bitwise_and(np.uint64(a), np.uint64(b))
		mask = np.bitwise_and(np.uint64(c), np.uint64(d))


		if debug:
			# cv2.imshow("original", im)
			cv2.imshow("debug_rgb", im)
			cv2.waitKey(0)

		return mask.astype(float)

	def ycrcb_mask(self, im, debug = False):
		assert isinstance(im, np.ndarray)
		assert im.ndim == 3

		ycrcb = cv2.cvtColor(im, cv2.COLOR_BGR2YCR_CB)
		mask = cv2.inRange(ycrcb, SKINCONSTS.YCRCB_LOWER, SKINCONSTS.YCRCB_UPPER)

		if debug:
			# cv2.imshow("original", im)
			cv2.imshow("ycrcb", mask)
			cv2.waitKey(0)

		return mask.astype(float)



	def get_skin(self, im, threshold = 0.5, debug = False):
		assert isinstance(im, np.ndarray)
		assert im.ndim == 3

		hsv = self.hsv_mask(im)
		rgb = self.rgb_mask(im)
		ycrcb = self.ycrcb_mask(im)

		mask = (hsv + rgb + ycrcb) / 3

		mask = mask.astype(np.uint8)

		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
		mask = cv2.erode(mask, kernel, iterations = 2)
		mask = cv2.dilate(mask, kernel, iterations = 2)
		mask = cv2.GaussianBlur(mask, (SKINCONSTS.BLUR_CONST, SKINCONSTS.BLUR_CONST), 0)

		# skin = cv2.bitwise_and(im, im, mask = mask)

		ret, thresh = cv2.threshold(mask, SKINCONSTS.BINARY_THRESH, 255, cv2.THRESH_BINARY)

		if debug:
			# cv2.imshow("original", im)
			# cv2.imshow("mask", mask)
			cv2.imshow("threshold", thresh)
			cv2.waitKey(0)

		return ret, thresh

	# def remove_bg(self, im, debug = False):
	# 	assert isinstance(im, np.ndarray)
	# 	assert im.ndim == 3

	# 	bgModel = cv2.createBackgroundSubtractorMOG2()
	# 	mask = bgModel.apply(im)

	# 	kernel = np.ones((3,3), np.uint8)
	# 	mask = cv2.erode(mask, kernel, iterations = 1)

	# 	res = cv2.bitwise_and(im, im, mask = mask)

	# 	if debug:
	# 		cv2.imshow("mask", mask)
	# 		cv2.waitKey(0)

	# 	return res







