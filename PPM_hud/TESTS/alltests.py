from PPM_hud.img_processing import *
from PPM_hud.input_user_utils import *
from PPM_hud.window_control import *
from PPM_hud.main import *


from ctypes import windll
import glob, os



# img_mesaReaded = cv2.imread('onlyTable_10577.png', 1)


# cv2.imshow('onetable',img_mesaReaded)

# cv2.waitKey(0)
cv2.waitKey(0)
# time.sleep(2)
# snapshoot()
#
# cv2.imshow('ALL SCREEN?',snapshoot())

def findtable_withIMG():
	pointOG_Coord_lst, tableBox_Coord_lst = setup_coordTableBox()

	print('Find', len(tableBox_Coord_lst), 'Tables')
	print(tableBox_Coord_lst)
	for num, tablebox_Coord in enumerate(tableBox_Coord_lst):

		tablebox_img = snapshoot(TL_point=tablebox_Coord[0], BR_point=tablebox_Coord[1])

		cv2.imshow('table{}'.format(num),tablebox_img)

		# find empty seats [true, false, true, true etc]
		empty_seats_lst = find_emptyseats(tablebox_img)

		print(empty_seats_lst)

		cv2.waitKey(0)




def emptyseat():
	img_mesaReaded = cv2.imread('onlyTable_10577.png', 1)

	cv2.imshow('onetable',img_mesaReaded)
	# find empty seats [true, false, true, true etc]
	empty_seats_lst = find_emptyseats(img_mesaReaded)

	print(empty_seats_lst)

	cv2.waitKey(0)


def clickIds():
	pointOG_Coord_lst, tableBox_Coord_lst = setup_coordTableBox()

	print('Find', len(tableBox_Coord_lst), 'Tables')

	for num, tablebox_Coord in enumerate(tableBox_Coord_lst):

		tablebox_img = snapshoot(TL_point=tablebox_Coord[0], BR_point=tablebox_Coord[1])

		# cv2.imshow('table{}'.format(num), tablebox_img)

		# find empty seats [true, false, true, true etc]
		empty_seats_lst = find_emptyseats(tablebox_img)

		# thepoint for click and get out idplayer window
		neutralpoint_screen = convert_Coord_TabletoGeneral(tablebox_Coord, coordonates8max.neuralpoint)
		# for know where to get the id img
		coordTLid = convert_Coord_TabletoGeneral(tablebox_Coord, coordonates8max.IDtl)
		coordBRid = convert_Coord_TabletoGeneral(tablebox_Coord, coordonates8max.IDbr)

		img_id_1table_lst = []

		for empty_seat, coordclick in zip(empty_seats_lst, coordonates8max.playersinfo):
			if empty_seat == False:
				coord_screen = convert_Coord_TabletoGeneral(tablebox_Coord, coordclick)

				# todo might be better set alias , name random , later read it and find if in list
				img_id = get_Img_IDplayer(coord_screen, neutralpoint_screen, coordTLid, coordBRid)
				# img_id_1table_lst.append(img_id)
			else:
				img_id_1table_lst.append(None)

		# print('Time take all image of table:{:.20}'.format(time.clock() - TimeStrated))



def OCRids():


	os.chdir(r"C:\Users\lapto\PycharmProjects\PPM_HUD\Tests\realID1/")
	for file in glob.glob("*"):
		readedID = cv2.imread(file, 1)


		r = 500.0 / readedID.shape[1]
		dim = (500, int(readedID.shape[0] * r))

		# perform the actual resizing of the image and show it
		resized = cv2.resize(readedID, dim, interpolation=cv2.INTER_AREA)
		# idididid = processOCR_Numbers(readedID)

		cv2.imshow('onetable', resized)
		cv2.waitKey(0)



def findtable_withNameWindow ():

	infowindow = search_window('memu')
	print(infowindow)
	# win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT, 0, win32con.SPIF_SENDWININICHANGE | win32con.SPIF_UPDATEINIFILE)
	win32gui.SetForegroundWindow(infowindow[0][0])
	win32gui.ShowWindow(infowindow[0][0], win32con.SW_RESTORE)

def findBacks():
	img_mesaReaded = cv2.imread('onlyTable_10122.png', 1)

	cv2.imshow('onetable', img_mesaReaded)
	basck_lst = find_backs(img_mesaReaded)
	print(basck_lst)
	cv2.waitKey(0)



findtable_withIMG()


# findtable_withNameWindow()
#
emptyseat()
#
#
clickIds()
#
findBacks()
OCRids()

