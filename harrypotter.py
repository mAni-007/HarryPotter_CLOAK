import cv2
import time
import numpy as np

#Just boring stuff need to compulsory
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20.0, (640,480))
cap = cv2.VideoCapture(0)
time.sleep(2)
count = 0
background = 0

## Capture the background in range of 60
for i in range(6):
    ret,background = cap.read()

while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    count+=1
    img = np.flip(img,axis=1)
    print ("gi")
    
    ## Convert the color space from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # ## Generat masks to detect red color
    # lower_red = np.array([0,120,50])
    # upper_red = np.array([10,255,255])
    # mask1 = cv2.inRange(hsv,lower_red,upper_red)

    # lower_red = np.array([170,120,70])
    # upper_red = np.array([180,255,255])
    # mask2 = cv2.inRange(hsv,lower_red,upper_red)

    # mask1 = mask1+mask2
    # Generat masks to detect skin color
    lower_skin = np.array([0,30,60])
    upper_skin = np.array([20,150,255])
    mask1 = cv2.inRange(hsv,lower_skin,upper_skin)

    lower_black = np.array([0,0,0])
    upper_black = np.array([179,50,100])
    mask2 = cv2.inRange(hsv,lower_black, upper_black)

    mask1 = mask1 + mask2



    ## Open and Dilate the mask image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
 
 
    ## Create an inverted mask to segment out the red color from the frame
    mask2 = cv2.bitwise_not(mask1)
 
 
    ## Segment the red color part out of the frame using bitwise and with the inverted mask
    res1 = cv2.bitwise_and(img,img,mask=mask2)

    ## Create image showing static background frame pixels only for the masked region
    res2 = cv2.bitwise_and(background, background, mask = mask1)
 
 
    ## Generating the final output and writing
    finalOutput = cv2.addWeighted(res1,1,res2,1,0)
    out.write(finalOutput)
    cv2.imshow("magic",finalOutput)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()