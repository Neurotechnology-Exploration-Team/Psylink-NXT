from psylink.protocol import BLEDecoder
from psylink.bluetooth import BLEGATTBackend
from psylink.config import IMU_CHANNELS
import time
import matplotlib.pyplot as plt
import matplotlib.animation as pltAnim
#Manually set channel count
channels = 8

bleb = BLEGATTBackend()
bled = BLEDecoder()

timeDelay = 2

bleb.connect()
bleb.thread_start()
#Decode channel count TODO: Implement channel count decoding
#channels =  bled.decode_channel_count();

bled.channels = channels + IMU_CHANNELS
bled.emg_channels = channels 

def loopBLE(bleb, bled):
    emgData = [[0]* bled.channels, 0]
    print("Starting bleb/bled loop")
    lastT = time.time()
    while(True):
        while (time.time() <= (lastT+timeDelay)):
            blebPipe = bleb.pipe.get()
        #print(blebPipe, end=" |:| ")
            bledPack = bled.decode_packet(blebPipe)
            if(not bledPack["is_duplicate"]):
                curSamples = bledPack["samples"]
                for sample in curSamples:
                    for chan_ind in range(bled.channels):
                        emgData[0][chan_ind] += abs(sample[chan_ind])
                    emgData[1] += 1
        if(emgData[1] == 0):
            print("0 Packets read")
            continue
        for chan_ind in range(bled.channels):
            emgData[0][chan_ind] /= emgData[1]
        print(emgData[0])
        emgData = [[0] * bled.channels,0]
        lastT = time.time()
	        #print(bledPack)

            

#TODO: Thread loopBLE
loopBLE(bleb, bled)
