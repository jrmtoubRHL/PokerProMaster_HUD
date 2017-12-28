from PPM_hud.img_processing import *
import pyautogui
import sys




#need to find tables,

def setup_coordTableBox():
	'''
	Find (Tables with pointsOGs), returns coordenate of tables (topleftx, toplefty ) y botomrightx, botomrighty
	pointOG = some visual object for reconize the table, (template matching)
	If pointOG there is a table.

	pointsOG_coord_lst = list of coords where the pointOGs was find
	tableBox_Coord_lst = list of corrdonates TopLeft and BotomRight of the tables,
	tableBox_Coord_lst = (((table1TLx, table1TLy), (table1BRx, table1BRy)) , ((table2TLx, table1TLy), (table2BRx, table2BRy)))
	:return: pointsOG_coord_lst , tableBox_Coord_lst
	'''
	# todo return witch site?

	# snapshoot all screen
	hole_scrn_img = snapshoot()

	# find point(s)OG  (for know how many and where are tables)
	pointsOG_coord_lst = find_Coord_PointsOG(hole_scrn_img)

	if not pointsOG_coord_lst:
		print('no table finded stop.')
		sys.exit()

	# each pointOG finded , find coordonates for crop tables
	tableBox_Coord_lst = get_Coord_TableBox(pointsOG_coord_lst)

	return pointsOG_coord_lst, tableBox_Coord_lst



def main():

	pointOG_Coord_lst, tableBox_Coord_lst = setup_coordTableBox()

	# print('Coordenates of tables finded: ' ,tableBox_Coord_lst)
	TimeStrated = time.clock()

	for tablebox_Coord in tableBox_Coord_lst:
		# tablebox_Coord ((627, 242), (1152, 1138))
		#get tablebox img



		#(pointOGxtl=tablebox_Coord[0][0], pointOGytl=tablebox_Coord[0][1], widthbox=withtablebox, heightbox=heighttablebox )
		tablebox_img = snapshoot(TL_point=tablebox_Coord[0] , BR_point=tablebox_Coord[1])
		# cv2.imshow('assd', tablebox_img)

		# find empty seats [true, false, true, true etc]
		empty_seats_lst = find_emptyseats(tablebox_img)

		# If no empty, click and get ID player (if empty it will seat..
		# print(empty_seats_lst) [False, True, False, False, False, False, False, True]
		# print(coordonates.playersinfo8max) [(250, 700), (55, 574), (50, 397), (53, 236), (242, 119), (437, 236), (433, 406), (433, 576)]

		#thepoint for click and get out idplayer window
		neutralpoint_screen = convert_Coord_TabletoGeneral(tablebox_Coord, coordonates8max.neuralpoint)
		#for know where to get the id img
		coordTLid =convert_Coord_TabletoGeneral(tablebox_Coord, coordonates8max.IDtl)
		coordBRid = convert_Coord_TabletoGeneral(tablebox_Coord, coordonates8max.IDbr)


		img_id_1table_lst = []

		for empty_seat, coordclick in zip(empty_seats_lst, coordonates8max.playersinfo8max):
			if empty_seat == False:
				coord_screen = convert_Coord_TabletoGeneral(tablebox_Coord , coordclick)

				# todo might be better set alias , name random , later read it and find if in list
				img_id = get_Img_IDplayer(coord_screen , neutralpoint_screen, coordTLid, coordBRid)
				img_id_1table_lst.append(img_id)
			else:
				img_id_1table_lst.append(None)


		print('Time take all image of table:{:.20}'.format(time.clock() -TimeStrated))




		for num,imID in enumerate(img_id_1table_lst):

			cv2.imwrite('id100{}.png'.format(time.clock()),imID)




	cv2.waitKey(0)

if __name__ == '__main__':
	main()