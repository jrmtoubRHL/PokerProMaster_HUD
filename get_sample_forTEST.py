#save img tables

from PPM_hud.img_processing import *






pointOG_Coord_lst, tableBox_Coord_lst = setup_coordTableBox()

tablebox_Coord = tableBox_Coord_lst[0]
# tablebox_Coord ((627, 242), (1152, 1138))
# get tablebox img
count = 10000
while (True):
	tablebox_img = snapshoot(TL_point=tablebox_Coord[0], BR_point=tablebox_Coord[1])

	#img = cv2.imread('messi5.jpg',0)
	#cv2.imshow('image',img)
	#cv2.waitKey(0)
	cv2.imwrite('onlyTable_{}.png'.format(count),tablebox_img)
	count += 1
	time.sleep(0.3)
	#img[y1:y2 , x1:x2]