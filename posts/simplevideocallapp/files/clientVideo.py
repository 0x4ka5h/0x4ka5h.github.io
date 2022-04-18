import cv2
import numpy as np
import sys
import time
import socket
import pickle

print("[*]Initializing socket for Video")

# video socket
soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("[*]Initializing webcam for Video")
#initilizing webcam for videosocket
video=cv2.VideoCapture(0)
print("[*]Initializtion of webcam access succed\n")

# connecting to video socket at 8080
print("[*] Creating open socket server at 8080 port for video")
soc.connect(('127.0.0.1',8080))
print("[*] Connected \n\n")

def sendVideo():
    global soc
    while 1:
        try:
            _,frame=video.read()
            img_data=np.array(frame)
            data=pickle.dumps(img_data)
            soc.send(b'a'+data)
        except KeyboardInterrupt:
            video.release()
            sys.exit()


def recvVideo():
    global soc
    while 1:
        try:
            data=b''
            length=0
            while length<921766:
                pac2=soc.recv(9999999)
                length+=len(pac2)
                data=data+pac2
            if data[0:1]==b'b':
	            frame2=pickle.loads(data[1::])
	            cv2.imshow("frame2",frame2)
	            key=cv2.waitKey(1)
	            if key==27:
	                break
        except KeyboardInterrupt:
            sys.exit()	
cv2.destroyAllWindows()
