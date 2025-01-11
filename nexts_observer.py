from screen_reader import ScreenReader
from mino_distincter import MinoDistincter
from constants import *

class NextsObserver:
	UNRELIABLE_MINOS = [None, Mino.I, Mino.J] # エフェクトで誤検出されやすいミノ
	def __init__(self, screen_reader: ScreenReader):
		self.screen_reader = screen_reader
		self.reset()
	
	def reset(self):
		self.last_nexts = [None for _ in range(NEXT_COUNT)]
		self.next_history = []

	def observe(self):
		frame = self.screen_reader.read()
		next_imgs = self.screen_reader.get_nexts(frame)

		nexts, has_mino_put, reset = self.get_nexts(next_imgs)
		self.last_nexts = nexts
		if reset:
			print("nexts reset")
			return True

		if has_mino_put:
			self.save_nexts(nexts)
				

		return False
	
	def get_nexts(self, next_imgs) -> tuple[list, bool, bool]: # ネクストが進んだか, ネクストのリスト
		raw_nexts = [] # 画像から検出したそのままのネクスト
		for next_img in next_imgs:
			next = MinoDistincter.distinct(next_img)
			raw_nexts.append(next)

		if raw_nexts.count(None) >= 3: # 信頼性の低いミノが多い場合
			print("too many unreliable minos")
			return self.last_nexts, False, True # リセット
		
		if self.last_nexts.count(None) == NEXT_COUNT: # 初回
			return raw_nexts, True, False
		is_unchanged = True # 変更がないか
		for i in range(NEXT_COUNT):
			# print(self.last_nexts[i], raw_nexts[i])
			if raw_nexts[i] in NextsObserver.UNRELIABLE_MINOS or \
			   self.last_nexts[i] in NextsObserver.UNRELIABLE_MINOS:
				continue
			if self.last_nexts[i] != raw_nexts[i]:
				is_unchanged = False
				break
		if is_unchanged:
			return raw_nexts, False, False
		
		is_proceeded = True # ミノが設置されてネクストが進んだか
		for i in range(NEXT_COUNT - 1):
			if raw_nexts[i] in NextsObserver.UNRELIABLE_MINOS or \
			   self.last_nexts[i+1] in NextsObserver.UNRELIABLE_MINOS: # 信頼性の低いミノは無視
				continue
			if raw_nexts[i] != self.last_nexts[i+1]: # 進んだわけじゃない場合
				is_proceeded = False
		if is_proceeded:
			next = []
			for i in range(NEXT_COUNT - 1):
				if(raw_nexts[i] == Mino.I and self.last_nexts[i+1] != Mino.I):
					next.append(self.last_nexts[i])
				else:
					next.append(raw_nexts[i] or self.last_nexts[i+1])
			next.append(raw_nexts[4])
			return next, True, False
		print("last:", self.last_nexts, " now:", raw_nexts)
		return raw_nexts, False, True # リセット
	
	def save_nexts(self, nexts):
		if len(self.next_history) < len(nexts):
			self.next_history.extend(nexts)
			return
		for i in range(len(nexts) - 1): # 4番目までを正しいネクストに修正
			former = self.next_history[-len(nexts) + i + 1] # もともとのネクスト
			if former == nexts[i]:
				continue
			if former in NextsObserver.UNRELIABLE_MINOS and \
				not (nexts[i] in NextsObserver.UNRELIABLE_MINOS):
				self.next_history[-len(nexts) + i + 1] = nexts[i]
			elif nexts[i] in NextsObserver.UNRELIABLE_MINOS and \
				not (former in NextsObserver.UNRELIABLE_MINOS):
				self.next_history[-len(nexts) + i + 1] = former
		self.next_history.append(nexts[-1]) # 最後のネクストを追加