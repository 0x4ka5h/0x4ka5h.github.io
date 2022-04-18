import serverVideo
import serverAudio
import time
from threading import Thread

print("[*] .... .")
print("[*] ...")

time.sleep(5)

print("[*] ..  .. ... Inititalizing completed ")
print("[*] ..  .. ... Starting threads ")

recvVideo = serverVideo.recvVideo
recvAudio = serverAudio.rcvAudio

sendVideo = serverVideo.sendVideo
sendAudio = serverAudio.recordAudio

recvV = Thread(target = recvVideo )
sendV = Thread(target = sendVideo)
recvA = Thread(target = recvAudio)
sendA = Thread(target = sendAudio)

recvA.start()
sendA.start()

recvV.start()
sendV.start()


