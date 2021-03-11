import cv2 ,time
import pandas
from datetime import datetime

df=pandas.DataFrame(columns=["Start","End"])

f_frame=None
video=cv2.VideoCapture(0,cv2.CAP_DSHOW)
status_list=[None,None]
times=[]

while True:
    check, frame=video.read()
    status=0

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(31,31),1)     #pm(image_name,(width ,height of gaussian curnal), standard_deviation=0). to blur the inage to get more accuracy

    if f_frame is None:
        f_frame=gray
        continue                               #continue to the begining of the loop.will not execute below code

    delta_frame=cv2.absdiff(f_frame,gray)
    thresh_frame=cv2.threshold(delta_frame,40,255,cv2.THRESH_BINARY)[1]     #pm(img_name,thresh_hold_limit,color of that pixcel[white=255],thershold_method)[1for THRESH_BINARY], to make black and white moving image
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=5)                 #pm(img_name,None,itertion=n) to smoothen the spots 

    (cnts,_)=cv2.findContours(thresh_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)      #pm(finding contors of which frame[copped],method for outline in frame, method)

    for contours in cnts:
        if cv2.contourArea(contours)<10000:           #limiting the area of the counters to draw recatngle
            continue
        status=1
        (x,y,w,h)=cv2.boundingRect(contours)         #getting the x,y,w,h of the rectangle of the contour
        cv2.rectangle(frame,(x,y,x+w,y+h),(0,255,0),3) #pm already done (img_name,(2 coordiates of rect),(R,G,B),width).drawing the rectangle around the contour
    status_list.append(status)

    status_list=status_list[-2:]

    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    cv2.imshow("gray frame",gray)
    cv2.imshow("deltaframe",delta_frame)
    cv2.imshow("threshhold frame",thresh_frame)
    cv2.imshow("object capture",frame)
    key=cv2.waitKey(1)

    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break
    
print(status_list)
print (times)

for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()



