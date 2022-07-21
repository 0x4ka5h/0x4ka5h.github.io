import cv2
import dlib
import numpy as np
import time
import os
import sys
cap=cv2.VideoCapture(0)
detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
blink=0
s=0
ear=0
wake_time,sleep_time,hensy,time_get=0,0,0,0
m=1
def calclus(l):
    x_d=(l[1][0]-l[5][0])**2
    y_d=(l[1][1]-l[5][1])**2
    p2_p6=np.sqrt(x_d+y_d)
    x_d=(l[2][0]-l[4][0])**2
    y_d=(l[2][1]-l[4][1])**2
    p3_p5=np.sqrt(x_d+y_d)
    x_d=(l[0][0]-l[3][0])**2
    y_d=(l[0][1]-l[3][1])**2
    p1_p4=np.sqrt(x_d+y_d)
    ratio=(p2_p6+p3_p5)/p1_p4
    return ratio
def capture():  
    global blink,detector,predictor,cap,ratio,ear,wake_time,time_get,s,start,end,time1,blink,thread,m,hensy,out
    while True:
        start=time.time()
        _,frame=cap.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=detector(gray)
        font=cv2.FONT_HERSHEY_SIMPLEX
        name="Blinks : "+str(blink)
        for face in faces:
            x=face.left()
            y=face.top()
            h=face.right()
            k=face.bottom()
            #cv2.rectangle(gray,(x,y),(h,k),(0,255,0),1)
            landmarks=predictor(gray,face)
    ################     eye1        ######################
            eye1=[]
            for n in range(36, 42):
                eye1.append(landmarks.part(n))
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(gray, (x, y), 1, (255, 0, 0), 0)
            eye=[]
            for i in eye1:
                p=str(i)
                try:
                    x=int(p[1:4].strip())
                    y=int(p[6:len(p)-1].strip())
                except:
                    x=int(p[1:3].strip())
                    y=int(p[5:len(p)-1].strip())
                eye.append([x,y])
            ratio1=calclus(eye)
            eye2=[]
    ################     eye2       ######################
            for n in range(42, 48):
                eye2.append(landmarks.part(n))
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(gray, (x, y), 1, (255, 0, 0), 0)
            eye=[]
            for i in eye2:
                p=str(i)
                try:
                    x=int(p[1:4].strip())
                    y=int(p[6:len(p)-1].strip())
                except:
                    x=int(p[1:3].strip())
                    y=int(p[5:len(p)-1].strip())
                eye.append([x,y])
            ratio2=calclus(eye)
            ear=(ratio1+ratio2)/4
            if(ear<=0.23):
                s=1
                if m==1:
                    m+=1
                    wake_time=time.time()
                time_get=time.time()
            elif(ear>=0.25 and s==1):
                blink+=1
                s+=1
                m=1
                #time_get=time.time()
            else:
                m=1
            hensy=abs(int(time_get-wake_time))
            if hensy>=5:
                cv2.putText(gray,"sleepy , get wake up ",(150,45),font,1,(255,255,255),1,cv2.LINE_AA)
                out=1
            else:
                out=0
                cv2.putText(gray,str(hensy),(450,75),font,1,(255,255,255),1,cv2.LINE_AA)

        cv2.putText(gray,name,(50,75),font,1,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(gray,str(ear)[0:4],(350,75),font,1,(255,255,255),1,cv2.LINE_AA)
        cv2.imshow("sample",gray)
        key=cv2.waitKey(1)
        if key==27:
            break
        if out==1:
            break
    cv2.destroyAllWindows()
    print(blink)
capture()
while out<=5:
    try:
        os.system("play alarm.mp3")
    except KeyboardInterrupt:
        break
    out+=1
cap.release()
