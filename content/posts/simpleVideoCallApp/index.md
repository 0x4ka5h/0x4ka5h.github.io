+++
title = "A Simple Video Call App with python Sockets"
description = "This project is used to communicating a person in local network"
date = 2020-01-20T07:34:48+08:30
featured = false
draft = false
comment = false
toc = false
reward = false
categories = [
  "Socket"
]
tags = [
  "ImageProcessing",
  "openCV"
]
series = []
images = ["images/1.png"]
+++
### Introduction 
Hey mates😊. How are you? Hope you all are begin good.By the way, This is my first blog. Did you know my name 🥱? Well, I am Akash.

#### Why we are here?
To make some fun? 😕! No, But we're here to learn something new in a funny way. Funny while learning😒? Yeah!.,

By the way, What's the new thing? Guess? 🤔🤔..  How to copy some code from StackOverflow easily using python? 😅, No. We are here to learn How to code **Simple VideoCall App with python sockets**.

VideoCall App? Android Application ah? No, Just a simple python interpreter application. But useful for future step😊.

#### About project ..!

This is a simple VideoCallApp created with python script using sockets and opencv. We are creating a simple TCP protocol using python sockets. We will read Video data from camera or webcam using opencv and Audio from microphone using pyAudio which are under Async function. I'm using two open ports to make communication between server and client. One port is for Video Transmission and one port is for Audio Transmission. I think by using two ports there will be no disturbances in socket communication.

#### Why I did this project ?
I think it's 2019 September. I was studying Engg-1. Most of my friends are using smartphones and I'm using a Jio smartPhone(KeyBoard phone).
I was very curious about networking at that time. My friends are doing Videochat with thier friends in smartphone, but I dont have one. One day I got this idea, why don't I made my own VideoCallingApp. I was already knew Image processing and openCV. So I can manage VideoStream and Audio too. That's why I decided to do this App.

#### Libraries
I'm using python to create this Application. Here are the list of libraries I had used to build this application
```python3
import cv2, numpy as np
import pyaudio
import socket

import pickle
import sys,time
```
 * Socket is python Library used to connect two nodes on a network to communicate with each other. One socket(node) listens on a particular port at an IP, while the other socket reaches out to the other to form a connection. The server forms the listener socket while the client reaches out to the server.
 * pyAudio is used to read and write data from microphone.
 * opencv is also used to read data from webcam

#### How to create socket and Bind connection
```python3
## serverside
simpleSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
simpleSocket.bind(('IP','PORT'))
simpleSocket.listen(5)
conn , addr = simpleSocket.accept()
conn.send(b"123 -- sent by server")

## clientSide
simpleSocket_ = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
simpleSocket_.connect(('IP','PORT'))
data = simpleSocket.recv(21)
print(str(data))
```
	b'123 -- sent by server'
This is the example of simple socket connection between a server and client. AF\_INET is the Internet address family for IPv4. SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport our messages in the network. 

#### Read data from webCam and MicroPhone
```python3
## reading data from webCamera
video = cv2.VideoCapture(0)
_, frame = video.read()
print(frame)
video.release()
cv2.destroyAllWindows()

## Reading data from microPhone
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
#initializing microphone
stream = p.open(format = FORMAT,
		channels = CHANNELS,
		rate = RATE,
		input = True,
		frames_per_buffer = chunk
		)

stream.read(chunk)
print(stream)
```
	prints ImageData in RGB array format 
	prints AudioData in 1D array format

#### Sending and Receiving Data from socket
```python3
#####################     ImageData      ################
## serverSide
length = 0
while length<921764:
	pac=simpleSocket.recv(9999999)
	length+=len(pac)
	data+=pac
receivedImage=pickle.loads(data)
## clientSide

img_data=np.array(frame)
data=pickle.dumps(img_data)
simpleSocket_.send(data)
```
```python3
####################      AudioData     #################
#serverSide
audioData = simpleSocket.recv(chunk)
audioData = pickle.loads(audioData)
stream.write(audioData)

#clientSide
data = stream.read(chunk)
if data:
    simpleSocket_.send(data)
```
	receivedImage => imageData is sent from client's socket and received to server's socket

	stream.write => audio data is read from microphone and sent from client's socket and received to server's socket and writes data on stream

That's it! We partially completed our main goal of the project. We received Image data and mircoPhone data from client to server for one time.

But the thing is, If we run a loop to send and retreive data from client to server its like first it sends image data and then microphone data. Again repeat..!. But we want Async data retreival from client to run video and audio simultaneously. So we use Threads to do this.

#### Async
```python3
#####################      ClientSide         #################
from threading import Thread
def recordAudio():
    time.sleep(5)
    while True:
        data = stream.read(chunk)
        if data:
            simpleSocket_.sendall(data)
def sendVideo():
    global conn,video
    while 1:
        try:
            _,frame=video.read()
            img_data=np.array(frame)
            data=pickle.dumps(img_data)
            conn.send(data)
        except KeyboardInterrupt:
            video.release()
            sys.exit()

sendVideo = serverVideo.sendVideo
sendAudio = serverAudio.recordAudio

sendV = Thread(target = sendVideo)
sendA = Thread(target = sendAudio)

recvA.start()
sendA.start()
```
```python3
#######################        serverSide           #################
from threading import Thread
def rcvAudio():
     while True:
          audioData = simpleSocket.recv(chunk)
          audioData = pickle.loads(audioData)
          stream.write(audioData)
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
            if data:
	            imgData=pickle.loads(data)
	            cv2.imshow("ClientData",imgData)
	            key=cv2.waitKey(1)
	            if key == 27:
	                break
        except KeyboardInterrupt:
            sys.exit()
recvVideo = serverVideo.recvVideo
recvAudio = serverAudio.rcvAudio


recvA = Thread(target = recvAudio)
recvV = Thread(target = recvVideo)

recvV.start()
sendV.start()
```
	Now, server gets continious data of Clients Video and Audio.

Now, We just have to write receieve functions for Image and Audio data in client side and sending function in serverside.

[simpleVideoCallApp](https://github.com/g00g1y5p4/simpleVideoCallApp/)

Hope you guys like and Subscribe to this Utube account 😂😂.

---
```
```
##### Thanks for reading! {align=center}
