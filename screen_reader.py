import cv2

from constants import *

class ScreenReader:
	HOLD_BEGIN = (138, 136)
	HOLD_SIZE = (48, 28)

	NEXTS_BEGIN = [(478, 109), (475, 162), (475, 213), (475, 263), (475, 314)]
	NEXTS_SIZE = (48, 28)

	FIELD_BEGIN = (206, 107)
	FIELD_SIZE = (240, 480)

	def __init__(self):
		self.cap = cv2.VideoCapture(5) # OBS Virtual Camera
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	
	def read(self):
		_, frame = self.cap.read()
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		return frame
	
	def get_hold(self, frame):
		cut_image = frame[
			self.HOLD_BEGIN[1]:self.HOLD_BEGIN[1] + self.HOLD_SIZE[1], 
			self.HOLD_BEGIN[0]:self.HOLD_BEGIN[0] + self.HOLD_SIZE[0]]
		return cut_image

	def get_field(self, frame):
		cut_image = frame[
			self.FIELD_BEGIN[1]:self.FIELD_BEGIN[1] + self.FIELD_SIZE[1], 
			self.FIELD_BEGIN[0]:self.FIELD_BEGIN[0] + self.FIELD_SIZE[0]]
		return cut_image

	def get_nexts(self, frame):
		cut_images = []
		for i in range(NEXT_COUNT):
			cut_image = frame[
				self.NEXTS_BEGIN[i][1]:self.NEXTS_BEGIN[i][1] + self.NEXTS_SIZE[1], 
				self.NEXTS_BEGIN[i][0]:self.NEXTS_BEGIN[i][0] + self.NEXTS_SIZE[0]]
			cut_images.append(cut_image)
		return cut_images

	def release(self):
		self.cap.release()
		cv2.destroyAllWindows()