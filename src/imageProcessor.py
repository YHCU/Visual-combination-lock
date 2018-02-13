import cv2

class imageProcessor(object):

	def __init__(self):
		pass
	
	def readImage(self, imgName):
		image = cv2.imread(imgName)

		ratio = 400.0 / image.shape[1]
		dim = (400, int(image.shape[0] * ratio))

		resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
		return resized_image

	def showImage(self, img):
		cv2.imshow("original", img)
		cv2.waitKey(0)