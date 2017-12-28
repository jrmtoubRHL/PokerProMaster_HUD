import win32gui
import win32con


def windowEnumerationHandler(hwnd, top_windows):
	rect = win32gui.GetWindowRect(hwnd)
	top_windows.append((hwnd, win32gui.GetWindowText(hwnd), (rect[2] - rect[0], rect[3] - rect[1]), (rect[0], rect[1]) , (rect[2], rect[3])))

###

def isRealWindow(hWnd):
	'''Return True if given window is a real Windows application window.'''
	if not win32gui.IsWindowVisible(hWnd):
		return False
	if win32gui.GetParent(hWnd) != 0:
		return False
	hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
	lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
	if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
		or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
		if win32gui.GetWindowText(hWnd):
			return True
	return False

def search_window(namewindow):
	'''
	Give title of window (contain) search and return some window properties ,

	#fixme Error in coordenates? 8pixel bigger?


	:param namewindow: Str name window contain (lower case always all )
	:return: (id_hWnd , 'name_window', (width, height) , (ToLeftx, TLy) ,
	(BottomRightx, BRy)
	'''
	resutlts = []
	top_windows = []
	win32gui.EnumWindows(windowEnumerationHandler, top_windows)
	for possible_window in top_windows:
		if namewindow in possible_window[1].lower():
			# print(i)
			if isRealWindow(possible_window[0]) == True:
				# print(possible_window)

				# win32gui.ShowWindow(possible_window[0], 5)
				# win32gui.SetForegroundWindow(possible_window[0])
				resutlts.append(possible_window)
	return resutlts


# print(search_window('notepad'))