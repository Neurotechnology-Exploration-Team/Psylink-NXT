from psylink.protocol import BLEDecoder
from psylink.bluetooth import BLEGATTBackend
from psylink.config import IMU_CHANNELS
#Manually set channel count
channels = 4

bleb = BLEGATTBackend()
bled = BLEDecoder()

bleb.connect()
bleb.thread_start()
#Decode channel count TODO: Implement channel count decoding
#channels =  bled.decode_channel_count();

bled.channels = channels + IMU_CHANNELS
bled.emg_channels = 4

def loopBLE(bleb, bled):
    print("Starting bleb/bled loop")
    while(True):
        blebPipe = bleb.pipe.get()
        print(blebPipe, end=" |:| ")
        bledPack = bled.decode_packet(blebPipe)
        print(bledPack)

#TODO: Thread loopBLE
loopBLE(bleb, bled)
