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
	}
	COLOR_UPPER = {
		Mino.I: (100, 255, 255),
	}

	def __init__(self):
		pass

	def distinct(self, frame):
		all_pixels = frame.size / 3 # 1pxあたり3要素
		for i in Mino:
			print(i)
		mask = cv2.inRange(frame, (85, 128, 128), (100, 255, 255)) # Iミノの色
		cv2.imwrite("hold_mask.jpg", mask)
		if cv2.countNonZero(mask) > all_pixels * 0.10: # 10%以上がそのミノの色
			mino = "I"
		else:
			mino = None
			print("rate: ", cv2.countNonZero(mask) / all_pixels)
		return mino

screenReader = ScreenReader()
minoDistincter = MinoDistincter()

frame = screenReader.read()
hold_img = screenReader.get_hold(frame)
hold_img_bgr = cv2.cvtColor(hold_img, cv2.COLOR_HSV2BGR)
cv2.imwrite("hold.jpg", hold_img_bgr)

hold_name = minoDistincter.distinct(hold_img)
print("Hold:", hold_name)

screenReader.release()