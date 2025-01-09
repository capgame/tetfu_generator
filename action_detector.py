import cv2

from screen_reader import ScreenReader
from mino_distincter import MinoDistincter
from constants import *

class ActionDetector:
	def __init__(self):
		self.screen_reader = ScreenReader()
		self.reset()
	
	def reset(self):
		self.last_field = None
		self.last_hold = None
		self.last_nexts = [None, None, None, None, None]
		self.current_mino = None

	def detect(self):
		frame = self.screen_reader.read()
		hold_img = self.screen_reader.get_hold(frame)
		field_img = self.screen_reader.get_field(frame)
		next_imgs = self.screen_reader.get_nexts(frame)

		hasMinoHold, hold = self.get_hold(hold_img)
		hasMinoPut, nexts = self.get_next(next_imgs)

		if hasMinoHold:
			if self.last_hold == None:
				pass
			else:
				self.current_mino = self.last_hold
			self.last_hold = hold
			# return Action.HOLD, hold
		if hasMinoPut:
			print(self.current_mino, "was put")
			self.current_mino = self.last_nexts[0]
			self.last_nexts = nexts

		return None
	
	def get_hold(self, hold_img) -> tuple[bool, Mino | None]: # ホールドが進んだか, ホールドのミノ
		hold = MinoDistincter.distinct(hold_img)
		if self.last_hold == hold:
			return False, hold
		return True, hold
	def get_next(self, next_imgs) -> tuple[bool, list]: # ネクストが進んだか, ネクストのリスト
		raw_nexts = [] # 画像から検出したそのままのネクスト
		for next_img in next_imgs:
			next = MinoDistincter.distinct(next_img)
			raw_nexts.append(next)

		if self.last_nexts == [None, None, None, None, None]: # 初回
			return True, raw_nexts

		unreliable_minos = [None, Mino.I] # エフェクトで誤検出されやすいミノ

		is_unchanged = True # 変更がないか
		for i in range(NEXT_COUNT):
			if raw_nexts[i] in unreliable_minos or self.last_nexts[i] in unreliable_minos: # 信頼性の低いミノは無視
				continue
			if raw_nexts[i] != self.last_nexts[i]: # 変更がある場合
				is_unchanged = False
		if is_unchanged:
			next = []
			for i in range(NEXT_COUNT):
				if raw_nexts[i] == Mino.I and not (self.last_nexts[i] in unreliable_minos):
					next.append(self.last_nexts[i]) # (I以外)→Iの場合のみIを無視
				else:
					next.append(raw_nexts[i] or self.last_nexts[i])
			return False, next
		
		is_proceeded = True # ミノが設置されてネクストが進んだか
		for i in range(NEXT_COUNT - 1):
			if raw_nexts[i] in unreliable_minos or self.last_nexts[i+1] in unreliable_minos: # 信頼性の低いミノは無視
				continue
			if raw_nexts[i] != self.last_nexts[i+1]: # 進んだわけじゃない場合
				is_proceeded = False
		if is_proceeded:
			next = []
			for i in range(NEXT_COUNT - 1):
				if(raw_nexts[i] == Mino.I and self.last_nexts[i+1] != Mino.I):
					next.append(self.last_nexts[i])
				next.append(raw_nexts[i] or self.last_nexts[i+1])
			next.append(raw_nexts[4])
			return True, next
		return True, raw_nexts # それ以外は設置とみなす
	
actionDetector = ActionDetector()
while True:
	actionDetector.detect()

	if cv2.waitKey(100) & 0xFF == ord('q'):
		break