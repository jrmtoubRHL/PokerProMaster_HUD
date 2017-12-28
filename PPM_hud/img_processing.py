import cv2
import numpy as np
import os
import win32gui, win32ui, win32con, win32api
import time
import pyautogui
from operator import add
from PIL import Image

from PPM_hud.input_user_utils import *

#Constants:

hwin = win32gui.GetDesktopWindow()
width_TOTscre = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height_TOTscre = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left_TOTscre = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top_TOTscre = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
hwindc = win32gui.GetWindowDC(hwin)
srcdc = win32ui.CreateDCFromHandle(hwindc)
memdc = srcdc.CreateCompatibleDC()


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


time_wait_screenshot_IDPLAYER = 0.40


# table could be find in diferents ways, on of them is looking at the entire
#  screen and find a caractereistic image
path_tablefinder = __location__ + '/templates/Pokerfish/tablefinder_1.bmp'
readed_tablefinder = cv2.imread(path_tablefinder, 1)


empty_path = __location__ + '/templates/Pokerfish/empty_seat.bmp'
emtpy_template_rd = cv2.imread(empty_path, 1)

path_Backs = __location__ + '/templates/Pokerfish/backs.png'
readed_backs = cv2.imread(path_Backs, 1)



class coordonates8max():
	# Usually TopLeftX , TopLeftY, )( BotomRightX, BottomRightY

	# where click for popup with playerID
	playersinfo = [(250, 700), (55, 574), (50, 397), (53,236) , (242, 119), (437, 236), (433, 406), (433, 576)]

	size_emptyseatWH = (120, 120)

	Emptyseat_TL_lst  = [(200, 649), (1 , 513) , (1, 323), (1, 159) , (191 , 51), (381, 163), (381, 327), (381, 517)]

	size_BacksArea = (70,70)

	BacksAreas_TL_lst = [(240, 696), (1, 568), (1, 393), (1, 226), (250, 118), (436, 226), (438, 396), (440, 571)]


	# EmptyseatBox = [size_emptyseatWH , (EmptyseatBoxtl[0], (EmptyseatBoxtl[0][0]) )]
	# EmptyseatBox = [size_emptyseatWH , (EmptyseatBoxtl[0],  )]



	# depedent of OG point, for get the tablebox from OGpoint
	tableBox_tl = (-19, -65)
	# tableBox_br =  1264 824 (OG = (825, 110)
	tableBox_br =  (506, 831)

	#whenclicked, where find the id
	IDtl = (176, 344)
	IDbr = (254, 357)

	neuralpoint= (351, 128)


# (TL_point = (left_TOTscre, top_TOTscre), BR_point=(width_TOTscre,height_TOTscre ) )
# (pointOGxtl=left_TOTscre, pointOGytl=top_TOTscre, widthbox=width_TOTscre, heightbox = height_TOTscre )
def snapshoot(TL_point = (left_TOTscre, top_TOTscre), BR_point=(width_TOTscre,height_TOTscre ) ):
	'''

	  0.09seg
	  works on various screens,
	  works even if coordonates are larger than the screen (complete empty
	  space with black)

	  ! By default , if no arg, it take screenshot of all

	:param pointOGxtl: x topleft take screenshot (default (0,0) all screen)
	:param pointOGytl: same same y ,
	:param widthbox: pretyy self explanatory
	:param heightbox:
	:return: img readable by opencv
	'''
	# TimeStrated = time.clock()

	bmp = win32ui.CreateBitmap()

	width =BR_point[0]-TL_point[0]
	height =BR_point[1]-TL_point[1]

	bmp.CreateCompatibleBitmap(srcdc, width, height)
	memdc.SelectObject(bmp)
	memdc.BitBlt((0, 0), (width, height), srcdc, (TL_point[0], TL_point[1]), win32con.SRCCOPY)

	# bmp.SaveBitmapFile(memdc, 'screenshot.bmp')
	bmpinfo = bmp.GetInfo()
	bmpstr = bmp.GetBitmapBits(True)
	PILimg = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)



	open_cv_image = np.array(PILimg)
	open_cv_image = open_cv_image[:, :, ::-1].copy()
	# print('Timescreenshot:{:.20}'.format(time.clock() - TimeStrated))

	return open_cv_image





def find_Coord_PointsOG(imgg):
	'''
	Find where is the template in image (table)
	:param imgg: big image
	:return: coordonates
	'''
	timestrattempalte = time.clock()

	threshold = 0.95
	res = cv2.matchTemplate(imgg, readed_tablefinder, cv2.TM_CCOEFF_NORMED)
	# cv2.imshow('image',readed_tablefinder)
	# cv2.imshow('image22',imgg)
	# cv2.waitKey(0)
	loc = np.where(res >= threshold)

	OGpoints_lst = []

	for pt in zip(*loc[::-1]):

		OGpoints_lst.append(pt)

	# print('I Find ', len(OGpoints_lst), 'table(s) with Coordonates: ', OGpoints_lst, '(Timed : ', time.clock() - timestrattempalte)
	return OGpoints_lst




def get_Coord_TableBox( OGpoint_lst):
	'''
	From the point we find table , it returns a hole box, witch is the
	entire table
	:param OGpoint_lst:
	:return:
	'''

	tables_coord_lst = []
	for point_origin in OGpoint_lst :
		table_tl = (point_origin[0]+coordonates8max.tableBox_tl[0] , coordonates8max.tableBox_tl[1]+point_origin[1])
		table_br = (point_origin[0]+coordonates8max.tableBox_br[0] , coordonates8max.tableBox_br[1]+point_origin[1])
		tables_coord_lst.append((table_tl, table_br))
		# table = img_general[table_tl[1]:table_br[1], table_tl[0]:table_br[0]]
		#
		# tables_imgs_lst.append(table)

	return tables_coord_lst


def crop_Img_TableBox(img_genreal, tableBox_coord):
	table = img_genreal[tableBox_coord[0][1]:tableBox_coord[1][1], tableBox_coord[0][0]:tableBox_coord[1][0]]
	return table



def convert_Coord_TabletoGeneral(coord_tablebox, pointtoconvert,  reverse=False):
	'''
	For know where to click etc, translate relative coord to absolute
	:param coord_tablebox:
	:param pointtoconvert:
	:param reverse:
	:return:
	'''
	if reverse == True:
		pass

	return (coord_tablebox[0][0]+pointtoconvert[0], coord_tablebox[0][1]+pointtoconvert[1])




def find_emptyseats(img):
	'''
	In the img of table, look for emptyseat, return a list
	:param img:
	:return: [True, False, False, False]
	'''
	is_empty_lst = []
	for area in coordonates8max.Emptyseat_TL_lst:
		img2find_empty = img[area[1]:area[1]+coordonates8max.size_emptyseatWH[1], area[0]:area[0]+coordonates8max.size_emptyseatWH[0]]
		# cv2.imshow('imGseatEmtpyoading ', img2find_empty)
		# cv2.imshow('templatemtpyoading ', emtpy_template_rd)
		# img2find_empty.astype(np.float32)
		# emtpy_template_rd.astype(np.float32)
		res = cv2.matchTemplate(img2find_empty, emtpy_template_rd, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		# print(max_val)
		if max_val >= 0.75:
			is_empty_lst.append(True)
		else:
			is_empty_lst.append(False)
	# print(time.clock()-timesttt)
	return is_empty_lst


def find_backs(img):
	'''
		In the img of table, look for backs (people with cards) , return a
		list
		:param img:
		:return: [True, False, False, False]
		'''
	# 0.1seg

	# timesttt = time.clock()
	playercards_lst = []
	for area in coordonates8max.BacksAreas_TL_lst:
		img2find = img[area[1]:area[1]+coordonates8max.size_BacksArea[1], area[0]:area[0]+coordonates8max.size_BacksArea[0]]
		# cv2.imshow('imGseatEmtpyoading ', img2find_empty)
		# cv2.imshow('templatemtpyoading ', emtpy_template_rd)
		# img2find_empty.astype(np.float32)
		# emtpy_template_rd.astype(np.float32)
		res = cv2.matchTemplate(img2find, readed_backs, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		# print(max_val)
		if max_val >= 0.50:
			playercards_lst.append(True)
		else:
			playercards_lst.append(False)
	# print(time.clock()-timesttt)
	return playercards_lst





def get_Img_IDplayer(coord_click, neutralpoint, coordTLid, coordBRid):

	'''

	:param coord_click: where to click for get the popup and see the id
	:param neutralpoint: where to click for cancel the popup (end)
	:param coordTLid:
	:param coordBRid:
	:return: img of the id, ready to apply OCR preprocessing
	'''

	# get the window ID up
	# pyautogui.click(button='left', x=coord_click[0], y=coord_click[1])
	click_homemade(coord_click)


	#wait
	time.sleep(time_wait_screenshot_IDPLAYER)

	id_img = snapshoot( TL_point=coordTLid, BR_point=coordBRid)


	# pyautogui.click(button='left', x=neutralpoint[0], y=neutralpoint[1])
	click_homemade(neutralpoint)
	time.sleep(time_wait_screenshot_IDPLAYER)


	return id_img