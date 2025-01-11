import cv2

from screen_reader import ScreenReader
from nexts_observer import NextsObserver

screenReader = ScreenReader()
nextsObserver = NextsObserver(screenReader)
while True:
	if nextsObserver.observe():
		for next in nextsObserver.next_history:
			print(next)
		nextsObserver.reset()

	if cv2.waitKey(100) & 0xFF == ord('q'):
		break