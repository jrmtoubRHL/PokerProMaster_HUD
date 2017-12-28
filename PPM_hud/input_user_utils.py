import win32gui, win32ui, win32con, win32api
import time
import pyautogui
import random
import threading


def click_homemade(coord_clikeable, thread=False):
	'''
	click some coordonate with some properties..:
	 -even if user is mooving the cursor manually,it go back once clicked is done
	 , at the same initial coordonates.

	Emulate effect 'simulation click without cursor moving'

	:param coord: (x,y) where to click
	:param thread: if true,
	:return:
	'''

	def zoomthread(coordonate2click):
		# get cursor position now
		xnow, ynow = pyautogui.position()
		# print(xnow, ynow)

		#click where coord_clikeable , and lock cursor (cant move it until clicked)
		win32api.ClipCursor((coordonate2click[0] - 1, coordonate2click[1] - 1, coordonate2click[0] + 1, coordonate2click[1] + 1))
		win32api.SetCursorPos((coordonate2click[0], coordonate2click[1]))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
		win32api.ClipCursor((0, 0, 0, 0))
		# move back the cursor where it was,
		win32api.SetCursorPos((xnow, ynow))


	if thread == False:
		zoomthread(coord_clikeable)

	else:

		t = threading.Thread(target=zoomthread, args=(coord_clikeable, ))
		t.daemon = True
		t.start()
