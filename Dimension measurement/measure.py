	
import cv2
import utlis
 
###################################
webcam = False 
path = '1.jpg'
#cap = cv2.VideoCapture(0)
#cap.set(10,160)
#cap.set(3,1920)
#cap.set(4,1080)
scale = 2
wP = 210 *scale
hP= 297 *scale
###################################
 
#while True:
#if webcam:
#    success,img = cap.read()
#else: 
img = cv2.imread('1.jpg')
img = cv2.resize(img, (620, 800))  # RESIZE IMAGE
cv2.imshow('Original',img)
cv2.waitKey(0) #shows original image until any key is pressed
imgContours , conts = utlis.getContours(img,filter=4)  #stores image and contour coordinates
if len(conts) != 0:
    
    biggest = conts[0][2] #stores largest dimension (A4 PAPER)
    
    imgWarp = utlis.warpImg(img, biggest, wP,hP) #crop
    cv2.imshow('A4',imgWarp) #shows warped image
    imgContours2, conts2 = utlis.getContours(imgWarp,minArea=2000, filter=4,cThr=[50,50],draw = False) #detect contours of the actual object
    if len(conts2) != 0:
        for obj in conts2:
            cv2.polylines(imgContours2,[obj[2]],True,(0,255,0),2)  #draw green contour line around object (width=2)
            nPoints = utlis.reorder(obj[2]) #rearranges contour points in ascending order
            nW = round((utlis.findDis(nPoints[0][0]//scale,nPoints[1][0]//scale)/10),1) #stores width
            nH = round((utlis.findDis(nPoints[0][0]//scale,nPoints[2][0]//scale)/10),1) #stores height of object 
            cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),(255, 0, 255), 3, 8, 0, 0.05) #width arrow
            cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),(255, 0, 255), 3, 8, 0, 0.05) #height arrow
            x, y, w, h = obj[3] #stores origin, width and height
            cv2.putText(imgContours2, '{}cm'.format(nW), (x + w//2, y + 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,(255, 0, 255), 2) #displays dimension along arrow
            cv2.putText(imgContours2, '{}cm'.format(nH), (x + 50, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,(255, 0, 255), 2)
    cv2.imshow('Final', imgContours2) #displays final image

cv2.waitKey(0)