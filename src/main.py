import imageProcessor as IP
import skindetector as SD
import gestureProcessor as GP
import cv2
import sys
import os

class ImageReadSession(object):

	def __init__(self, processor):
		self.processor = processor

	def read(self, image_path_list):
		image_list = {}
		for image_path in image_path_list:
			img = self.processor.readImage(image_path)
			image_list[image_path] = img
		return image_list		


def process_image(skinDetector, gestureProcessor, im):

	what = "unknown"
	where = "not visible"
	passRound = False
	ret, thresh = skinDetector.get_skin(im)
	found_contour, res, drawing = gestureProcessor.find_contour(thresh)
	if found_contour:
		found_fingers, num_fingers = gestureProcessor.num_fingers(thresh, res, drawing)
		if found_fingers:
			where = "visible"
			if num_fingers == 1:
				what = "Scissor"
			elif num_fingers == 4:
				what = "Paper"
			elif num_fingers == 0:
				what = "Rock"
	return what, where

def main():

	try:
		s_id = int(sys.argv[1])
	except:
		print("Incorrect sequence ID format.")
	if s_id == 0:
		skinDetector = SD.skinDetector()
		gestureProcessor = GP.gestureProcessor()
		camera = cv2.VideoCapture(0)

		while camera.isOpened():
		    ret, frame = camera.read()
		    frame = cv2.flip(frame, 1)
		    cv2.rectangle(frame, (int(0.5 * frame.shape[1]), 0), (frame.shape[1], int(0.8*frame.shape[0])), (0, 255, 0), 2)
		    cv2.imshow('frame', frame)

		    key = cv2.waitKey(10)
		    if key == ord('c'):
		    	crop_frame = frame[0:int(0.8 * frame.shape[0]), int(0.5 * frame.shape[1]):frame.shape[1]]
		    	what, where = process_image(skinDetector, gestureProcessor, crop_frame)
		    	print("Gesture: " + what + ", " + where)
		    elif key == ord('q'):
		    	break

	else:
		image_path_list = ["../imgs/Sequences/"+ str(s_id) + "/1.jpg", "../imgs/Sequences/"+ str(s_id) + "/2.jpg", "../imgs/Sequences/"+ str(s_id) + "/3.jpg"]
		passes = [False, False, False]

		if (os.path.exists("../imgs/Sequences/" + str(s_id) + "/")):
			if (os.path.exists(image_path_list[0])) and \
			(os.path.exists(image_path_list[1])) and \
			(os.path.exists(image_path_list[2])):
				processor = IP.imageProcessor()
				session = ImageReadSession(processor)

				image_list = {}
				image_list = session.read(image_path_list)

				print("Gesture inputs found. Processing...")
				

				skinDetector = SD.skinDetector()
				gestureProcessor = GP.gestureProcessor()

				## Predefined Sequence: Papar, Rock, Rock

				what, where = process_image(skinDetector, gestureProcessor, image_list[image_path_list[0]])
				if (what == "Rock") or (what == "Paper"):
					passes[0] = True

				print("Gesture 1:" + str(what) + "," + str(where))

				what, where = process_image(skinDetector, gestureProcessor, image_list[image_path_list[1]])
				if (what == "Rock") or (what == "Paper"):
					passes[1] = True

				print("Gesture 2:" + str(what) + "," + str(where))

				what, where = process_image(skinDetector, gestureProcessor, image_list[image_path_list[2]])
				if (what == "Rock") or (what == "Scissor"):
					passes[2] = True

				print("Gesture 3:" + str(what) + "," + str(where))

				if passes[0] and passes[1] and passes[2]:
					print("Accepted sequence.")
				else:
					print("Sequence not accepted.")
			else:
				print("Gesture inputs not found.")
		else:
			print("Sequence ID not found.")




	# processor = IP.imageProcessor()
	# session = ImageReadSession(processor)

	# # single image test
	# image_path_list = ["../imgs/Sequences/2.jpg"]
	# image_list = {}
	# image_list = session.read(image_path_list)

	# # single image test
	# Scissor = image_list[image_path_list[0]]

	# skinDetector = SD.skinDetector()
	# # hsv_mask = skinDetector.hsv_mask(Scissor, debug = True)
	# # rgb_mask = skinDetector.rgb_mask(Scissor, debug = True)
	# # ycrcb_mask = skinDetector.ycrcb_mask(Scissor, debug = True)
	# # skin = skinDetector.remove_bg(Scissor, debug = True)
	# ret, thresh = skinDetector.get_skin(Scissor)

	# gestureProcessor = GP.gestureProcessor()

	# found_contour, res, drawing = gestureProcessor.find_contour(thresh)
	# found_fingers, num_fingers = gestureProcessor.num_fingers(thresh, res, drawing, debug = True)


if __name__ == '__main__':
	main()