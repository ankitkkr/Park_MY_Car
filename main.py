import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture('vid_2.webm')
# print(cap.shape)

color=(255,0,255)
thickness=2

width, height = 63, 104

with open('carposition','rb') as f:
		position = pickle.load(f)

def checkParkingSpace(imgprocess):
	space = 0
	for pos in position:
		x,y = pos
		imgCrop = imgprocess[y:y+height,x:x+width]
		# cv2.imshow(str(x*y),imgCrop)
		count=cv2.countNonZero(imgCrop)
		cvzone.putTextRect(img,str(count),(x,y+height-90),scale=1,thickness=2,offset=0)

		if count<850:
			color = (0,255,0)
			thickness=5
			space += 1

		else:
			color = (0,0,255)
			thickness=2
		cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),color,thickness)

	cvzone.putTextRect(img,str(space),(580,100),scale=5,thickness=5,offset=10,colorR=(0,255,0))




while True:

	if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
		cap.set(cv2.CAP_PROP_POS_FRAMES,0)

	success, img = cap.read()
	img = cv2.resize(img, (1245,692))
	imggray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	imgblur = cv2.GaussianBlur(imggray,(3,3),3)
	imgthreshold = cv2.adaptiveThreshold(imgblur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
	imgmedian = cv2.medianBlur(imgthreshold,5)
	
	kernal = np.ones((3,3),np.uint8)
	imgdilate = cv2.dilate(imgmedian,kernal,iterations=1)

	checkParkingSpace(imgdilate)

	# for pos in position:
	# 	cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),color,thickness)


	cv2.imshow('Image',img)
	# cv2.imshow('Imageblur',imgblur)
	# cv2.imshow('Imagedialte',imgdilate)


	cv2.waitKey(200)
