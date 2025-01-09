import cv2

from constants import *
	
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
		Mino.T: (160, 255, 255),
		Mino.J: (120, 255, 255),
		Mino.S: (60, 255, 255),
	}

	@staticmethod
	def distinct(frame):
		all_pixels = frame.size / 3 # 1pxあたり3要素
		
		most_similar_mino = None
		similarity_rate = 0.15
		for mino in Mino:
			lower = MinoDistincter.COLOR_LOWER[mino]
			upper = MinoDistincter.COLOR_UPPER[mino]
			if(upper[0] < lower[0]): # 赤色の場合
				mask_a = cv2.inRange(frame, lower, (180, 255, 255))
				mask_b = cv2.inRange(frame, (0, 128, 128), upper)
				mask = cv2.bitwise_or(mask_a, mask_b)
			else:
				mask = cv2.inRange(frame, lower, upper)
			# print(mino, cv2.countNonZero(mask) / all_pixels)
			rate = cv2.countNonZero(mask) / all_pixels
			if rate > similarity_rate: # 類似度最大
				most_similar_mino = mino
	
		return most_similar_mino