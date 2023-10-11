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

fig = plt.figure()
axa = fig.add_subplot(1,1,1)
axb = fig.add_subplot(2,1,1, sharex=axa)
axc = fig.add_subplot(3,1,1, sharex=axa)
axd = fig.add_subplot(4,1,1, sharex=axa)
xs = []
axes = [[axa,[]],[axb,[]],[axc,[]],[axd,[]]]
bled.channels = channels + IMU_CHANNELS
bled.emg_channels = 4
emgData = [[0,0,0,0],0]
def loopBLE(bleb, bled, emgData, xs, axes):
    print("Starting bleb/bled loop")
    lastT = time.time()
    while(True):
        while(time.time() <= lastT+timeDelay):
            blebPipe = bleb.pipe.get()
            #print(blebPipe, end=" |:| ")
            bledPack = bled.decode_packet(blebPipe)
            if(not bledPack["is_duplicate"]):
                   # print(bledPack)
                curSamples = bledPack["samples"]
                for sample in curSamples:
                    emgData[0][0] += abs(sample[0])
                    emgData[0][1] += abs(sample[1])
                    emgData[0][2] += abs(sample[2])
                    emgData[0][3] += abs(sample[3])
                    emgData[1] += 1

        xs.append(time.time())
        xs = xs[-20:]
        
        curEmg = emgData
        emgData = [[0,0,0,0],0]
        curEmg[0][0] /= curEmg[1]
        curEmg[0][1] /= curEmg[1]
        curEmg[0][2] /= curEmg[1]
        curEmg[0][3] /= curEmg[1]
        for j in range(4):
            axes[j][1].append(curEmg[0][j])
            axes[j][1] = axes[j][1][-20:]
        for ax in axes:
            ax[0].clear()
            ax[0].plot(xs, ax[1])

        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)



#TODO: Thread loopBLE
#loopBLE(bleb, bled)
#ani = pltAnim.FuncAnimation(fig, loopBLE, fargs=(bleb, bled, emgData, xs, axes), interval=1000, repeat=False)
plt.show(block=False)
#loopBLE(bleb, bled, emgData, xs, axes)

print("Starting bleb/bled loop")
lastT = time.time()
while(True):
    while(time.time() <= lastT+timeDelay):
        blebPipe = bleb.pipe.get()
            #print(blebPipe, end=" |:| ")
        bledPack = bled.decode_packet(blebPipe)
        if(not bledPack["is_duplicate"]):
                   # print(bledPack)
            curSamples = bledPack["samples"]
            for sample in curSamples:
                emgData[0][0] += abs(sample[0])
                emgData[0][1] += abs(sample[1])
                emgData[0][2] += abs(sample[2])
                emgData[0][3] += abs(sample[3])
                emgData[1] += 1
    
    xs.append(time.time())
    xs = xs[-20:]
        
    curEmg = emgData
    emgData = [[0,0,0,0],0]
    curEmg[0][0] /= curEmg[1]
    curEmg[0][1] /= curEmg[1]
    curEmg[0][2] /= curEmg[1]
    curEmg[0][3] /= curEmg[1]
    for j in range(4):
        axes[j][1].append(curEmg[j][0])
        axes[j][1] = axes[j][1][-20:]
    for ax in axes:
        ax[0].clear()
        ax[0].plot(xs, ax[1])
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    lastT = time.time()
