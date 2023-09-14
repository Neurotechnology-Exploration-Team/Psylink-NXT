from psylink.protocol import BLEDecoder
from psylink.bluetooth import BLEGATTBackend
from psylink.config import IMU_CHANNELS
import time
import matplotlib.pyplot as plt
import matplotlib.animation as pltAnim
#Manually set channel count
channels = 4

bleb = BLEGATTBackend()
bled = BLEDecoder()

timeDelay = 2

bleb.connect()
bleb.thread_start()
#Decode channel count TODO: Implement channel count decoding
#channels =  bled.decode_channel_count();

bled.channels = channels + IMU_CHANNELS
bled.emg_channels = 4

def loopBLE(bleb, bled):
    emgShit = [[0,0,0,0], 0]
    print("Starting bleb/bled loop")
    lastT = time.time()
    while(True):
        while (time.time() <= (lastT+timeDelay)):
            blebPipe = bleb.pipe.get()
        #print(blebPipe, end=" |:| ")
            bledPack = bled.decode_packet(blebPipe)
            if(not bledPack["is_duplicate"]):
               # print(bledPack)
                curSamples = bledPack["samples"]
                for sample in curSamples:
                    emgShit[0][0] += abs(sample[0])
                    emgShit[0][1] += abs(sample[1])
                    emgShit[0][2] += abs(sample[2])
                    emgShit[0][3] += abs(sample[3])
                    emgShit[1] += 1
        if(emgShit[1] == 0):
            print("0 Packets read")
            continue
        emgShit[0][0] /= emgShit[1]
        emgShit[0][1] /= emgShit[1]
        emgShit[0][2] /= emgShit[1]
        emgShit[0][3] /= emgShit[1]
        print(emgShit[0])
        emgShit = [[0,0,0,0],0]
        lastT = time.time()
	        #print(bledPack)

            

#TODO: Thread loopBLE
loopBLE(bleb, bled)
