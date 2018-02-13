import cv2
import copy
import numpy as np
import math

class gestureProcessor(object):

	def __init__(self):
		pass

	def find_contour(self, threshold, debug = False):
		threshold_tmp = copy.deepcopy(threshold)
		contours = {}
		hierarchy = {}
		im_tmp, contours, hierarchy = cv2.findContours(threshold_tmp, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		max_area = -1
		max_index = -1
		if len(contours) > 0:
			for i in range(len(contours)):
				area = cv2.contourArea(contours[i])
				if area > max_area:
					max_area = area
					max_index = i

			res = contours[max_index]
			hull = cv2.convexHull(res)
			drawing = np.zeros(threshold_tmp.shape, np.uint8)
			cv2.drawContours(drawing, [res], 0, (0, 255, 0), 0)
			cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)

			if debug:
				# print("Number of convex hull edges:", len(hull))
				cv2.imshow("contour_output", drawing)
				cv2.waitKey(0)

			return True, res, drawing
		return False, 0, 0

	def num_fingers(self, threshold, res, drawing, debug = False):
		threshold_tmp = copy.deepcopy(threshold)
		hull = cv2.convexHull(res, returnPoints = False)
		# print(len(hull))
		if len(hull) > 3:

			# print("num of edges in numfingers", len(hull))

			defects = cv2.convexityDefects(res, hull)
			if type(defects) != type(None):

				num = 0
				for i in range(defects.shape[0]): # calculate angle
					start, end, far, _ = defects[i][0]
					start = tuple(res[start][0])
					end = tuple(res[end][0])
					far = tuple(res[far][0])
					a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
					b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
					c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
					angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
					if angle <= math.pi / 2:
						num += 1
						if debug:
							cv2.circle(threshold_tmp, far, 8, [211, 84, 0], -1)
					if debug:
						cv2.line(threshold_tmp, start, end, [100, 255, 100], 4, cv2.FILLED)


				if debug:
					cv2.imshow("output", threshold_tmp)
					# print("Num of fingers:", num)
					cv2.waitKey(0)

				return True, num

		return False, 0
