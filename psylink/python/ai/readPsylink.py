from psylink.protocol import BLEDecoder
from psylink.bluetooth import BLEGATTBackend
from psylink.config import IMU_CHANNELS, DEFAULT_BLE_ADDRESS
import threading

class Psylink_Thread:
    def __init__(self, channels, linux=True, mac=DEFAULT_BLE_ADDRESS){
        self.bled = BLEDecoder()
        if(linux):
            self.bleb = BLEGATTBackend(mac)
        else:
            self.bleb = BLEGATTBackend(mac)
            #TODO: Implement windows backend
        self.bleb.connect()
        self.bleb.thread_start()
        self.bled.channels = channels + IMU_CHANNELS
        self.bled.emg_channels = channels
        self.thread = None
        self.queue = queue.Queue()
        self.isThread = False

    def init_thread(self):
        self.thread = threading.thread(pl_thread)
        if(self.thread != None):
            self.isThread = True
            return True
        return False
    
    def close_thread(self):
        

    def pl_thread(self):
        emgSamples = [[0,0,0,0], 0, 0, 0]
        print("Starting bleb/bled loop")
        while(True):
            blebPipe = bleb.pipe.get()
            #print(blebPipe, end=" |:| ")
            bledPack = bled.decode_packet(blebPipe)
            if(not bledPack["is_duplicate"]):
               # print(bledPack)
                emgSamples[2] = datetime.now()
                curSamples = bledPack["samples"]
                for sample in curSamples:
                    emgSamples[0][0] += abs(sample[0])
                    emgSamples[0][1] += abs(sample[1])
                    emgSamples[0][2] += abs(sample[2])
                    emgSamples[0][3] += abs(sample[3])
                    emgSamples[1] += 1
                emgSamples[0][0] /= emgSamples[1]
                emgSamples[0][1] /= emgSamples[1]
                emgSamples[0][2] /= emgSamples[1]
                emgSamples[0][3] /= emgSamples[1]
                emgSamples[3] = datetime.now()
                self.queue.put(emgSamples, block=False)
                emgSamples = [[0,0,0,0],0, 0, 0]  

    def file_thread(self):
        while(True):
            if(self.queue.isEmpty()):
                continue
            samples = []
            while(not self.queue.isEmpty()):
                samples.append(self.queue.get(block=False))
            with open("ai/psylink_data.csv", "a+") as f:
                f.writelines(samples)
