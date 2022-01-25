import cv2
import pickle



width, height = 63, 104

try:
	with open('carposition','rb') as f:
		position = pickle.load(f)
except:
	position = []


def mouseclick(events,x,y,flags,params):
	if events == cv2.EVENT_LBUTTONDOWN:
		position.append((x,y))

	if events == cv2.EVENT_RBUTTONDOWN:
		for i, pos in enumerate(position):
			x1,y1=pos
			if x1< x <x1+width and y1<y<y1+height:
				position.pop(i)

	with open('carposition','wb') as f:
		pickle.dump(position,f)




while True:



	img=cv2.imread('vid_img.png')

	for pos in position:
		cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)




	cv2.imshow('Image',img)
	
	cv2.setMouseCallback('Image',mouseclick)
	cv2.waitKey(1)