from psylink.protocol import BLEDecoder
from psylink.bluetooth import BLEGATTBackend
from psylink.config import IMU_CHANNELS, DEFAULT_BLE_ADDRESS

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

    def pl_thread(self):
        emgShit = [[0,0,0,0], 0, 0, 0]
        print("Starting bleb/bled loop")
        while(True):
            blebPipe = bleb.pipe.get()
            #print(blebPipe, end=" |:| ")
            bledPack = bled.decode_packet(blebPipe)
            if(not bledPack["is_duplicate"]):
               # print(bledPack)
                emgShit[2] = time.time()
                curSamples = bledPack["samples"]
                for sample in curSamples:
                    emgShit[0][0] += abs(sample[0])
                    emgShit[0][1] += abs(sample[1])
                    emgShit[0][2] += abs(sample[2])
                    emgShit[0][3] += abs(sample[3])
                    emgShit[1] += 1
                emgShit[0][0] /= emgShit[1]
                emgShit[0][1] /= emgShit[1]
                emgShit[0][2] /= emgShit[1]
                emgShit[0][3] /= emgShit[1]
                emgShit[3] = time.time()
                self.queue.put(emgShit)
                emgShit = [[0,0,0,0],0, 0, 0]   
