import clientVideo
import clientAudio
import time
from threading import Thread

print("[*] .... .")
print("[*] ...")

time.sleep(5)

print("[*] ..  .. ... Inititalizing completed ")
print("[*] ..  .. ... Starting threads ")

recvVideo = clientVideo.recvVideo
recvAudio = clientAudio.rcvAudio

sendVideo = clientVideo.sendVideo
sendAudio = clientAudio.recordAudio

recvV = Thread(target = recvVideo )
sendV = Thread(target = sendVideo)
recvA = Thread(target = recvAudio)
sendA = Thread(target = sendAudio)

recvA.start()
sendA.start()

recvV.start()
sendV.start()


