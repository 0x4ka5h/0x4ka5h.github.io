import pyaudio
import time
import socket
import pickle
#audio socket

print("[*]Initializing socket for Audio output\n\n")
audioSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("[*] Creating open socket server at 5050 port for audio")
## connecting to audio socket at 5050
audioSocket.bind(("0.0.0.0",5050))
audioSocket.listen(5)
cAudio, addr_ = audioSocket.accept()
print("[*] Connected \n")

print("[*]Accessing mircophone")
#audio socket
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
#initializing microphone for audio socket
stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = chunk)


print("[*]Succesfully accessed")
print("[*]... ..")

def recordAudio():
    time.sleep(5)
    while True:
        data = stream.read(chunk)
        if data:
            cAudio.sendall(data)
            
def rcvAudio():
     while True:
          audioData = audioSocket.recv(chunk)
          audioData = pickle.loads(audioData)
          stream.write(audioData)

