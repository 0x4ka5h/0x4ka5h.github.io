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
soc.bind(('0.0.0.0',8080))
soc.listen(5)
conn,addr=soc.accept()
print("[*] Connected \n\n")

def recvVideo():
    global conn
    while 1:
        try:
            data=b""
            length=0
            while length<921764:
                pac=conn.recv(9999999)
                length+=len(pac)
                data+=pac
            if data[0:1]==b'a':
	            frame1=pickle.loads(data[1::])
	            cv2.imshow("frame1",frame1)
	            key=cv2.waitKey(1)
	            if key == 27:
	                break
        except KeyboardInterrupt:
            sys.exit()
            

def sendVideo():
    global conn,video
    while 1:
        try:
            _,frame=video.read()
            img_data=np.array(frame)
            data=pickle.dumps(img_data)
            conn.send(b"b"+data)
        except KeyboardInterrupt:
            video.release()
            sys.exit()
cv2.destroyAllWindows()
