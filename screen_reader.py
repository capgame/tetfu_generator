import numpy as np
import cv2

from constants import *

class ScreenReader:
	HOLD_BEGIN = (138, 136)
	HOLD_SIZE = (48, 28)

	NEXTS_BEGIN = [(478, 109)]
	NEXTS_SIZE = (48, 28)

	def __init__(self):
		self.cap = cv2.VideoCapture(5) # OBS Virtual Camera
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	
	def read(self):
		_, frame = self.cap.read()
		return frame
	
	def get_hold(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		cut_image = frame[
			self.HOLD_BEGIN[1]:self.HOLD_BEGIN[1] + self.HOLD_SIZE[1], 
			self.HOLD_BEGIN[0]:self.HOLD_BEGIN[0] + self.HOLD_SIZE[0]]
		

		return cut_image

	def get_field(self):
		pass

	def get_nexts(self):
		pass
	
	def render(self):
		frame = self.read()
		# cv2.rectangle(frame, 
		# 	self.HOLD_BEGIN, (self.HOLD_BEGIN[0] + self.HOLD_SIZE[0], self.HOLD_BEGIN[1] + self.HOLD_SIZE[1]),
		# 	(0, 0, 255), 1)
		# cv2.imshow("Game", frame)
		# cv2.imwrite("image.jpg", frame)

	def release(self):
		self.cap.release()
		cv2.destroyAllWindows()
	
class MinoDistincter:
	COLOR_LOWER = {
		Mino.I: (85, 128, 128),
		Mino.L: (10, 128, 128),
		Mino.O: (20, 128, 128),
		Mino.Z: (170, 128, 128),
		Mino.T: (140, 128, 128),
		Mino.J: (105, 128, 128),
		Mino.S: (40, 128, 128),
	}
	COLOR_UPPER = {
		Mino.I: (100, 255, 255),
		Mino.L: (15, 255, 255),
		Mino.O: (30, 255, 255),
		Mino.Z: (7, 255, 255),
		Mino.T: (150, 255, 255),
		Mino.J: (120, 255, 255),
		Mino.S: (60, 255, 255),
	}

	def __init__(self):
		pass

	def distinct(self, frame):
		all_pixels = frame.size / 3 # 1pxあたり3要素
		
		most_similar_mino = None
		similarity_rate = 0.15
		for mino in Mino:
			lower = self.COLOR_LOWER[mino]
			upper = self.COLOR_UPPER[mino]
			if(upper[0] < lower[0]): # 赤色の場合
				mask_a = cv2.inRange(frame, lower, (180, 255, 255))
				mask_b = cv2.inRange(frame, (0, 128, 128), upper)
				mask = cv2.bitwise_or(mask_a, mask_b)
			else:
				mask = cv2.inRange(frame, lower, upper)
			# cv2.imwrite("hold_mask.jpg", mask)
			rate = cv2.countNonZero(mask) / all_pixels
			# print(mino, ": ", rate)
			if rate > similarity_rate: # 類似度最大
				most_similar_mino = mino
	
		return most_similar_mino

screenReader = ScreenReader()
minoDistincter = MinoDistincter()

frame = screenReader.read()
hold_img = screenReader.get_hold(frame)
hold_img_bgr = cv2.cvtColor(hold_img, cv2.COLOR_HSV2BGR)
# cv2.imwrite("hold.jpg", hold_img_bgr)

hold_name = minoDistincter.distinct(hold_img)
print("Hold:", hold_name)

screenReader.release()