# WARNING: DO NOT EDIT "block_BLE_source.py" DIRECTLY! IT IS AUTOGENERATED BY GNURADIO!
# INSTEAD, OPEN GNURADIO, DOUBLE-CLICK THE BLOCK, AND CLICK ON "Open in Editor"!

import importlib
import os.path
import sys

import numpy as np
from gnuradio import gr

try:
    import psylink.bluetooth
    import psylink.protocol
except ImportError:
    # NOTE: You may need to change this path to where you downloaded psyink to:
    libpath = os.path.expanduser('~/repos/psylink/python')
    sys.path.insert(0, libpath)
    import psylink.bluetooth
    import psylink.protocol

DEFAULT_BLE_ADDRESS = 'A6:B7:D0:AE:C2:76'
EMG_CHANNELS = 8
SIGNAL_COUNT = EMG_CHANNELS + psylink.config.IMU_CHANNELS

class BLESource(gr.basic_block):
    def __init__(self, ble_mac=DEFAULT_BLE_ADDRESS):
        gr.basic_block.__init__(self, name='BLE Source', in_sig=[], out_sig=[np.float32] * SIGNAL_COUNT)
        self.ble_mac = ble_mac
        self.last_sample_count = 2048  # some large conservative value
        self.BLE = None
        self.BLE_decoder = psylink.protocol.BLEDecoder(sample_value_offset=0)
        self.actual_channels = SIGNAL_COUNT  # will be updated with data from device

    def general_work(self, input_items, output_items):
        count = 0
        pipe = self.BLE.pipe
        limit = len(output_items[0]) - self.last_sample_count
        while not pipe.empty() and count < limit:
            packet = pipe.get()
            data = self.BLE_decoder.decode_packet(packet)
            samples = data['samples']
            transposed = np.transpose(samples)
            for channel_id in range(min(SIGNAL_COUNT, self.actual_channels)):
                channel = output_items[channel_id]
                channel[count:count+len(samples)] = transposed[channel_id] / 256
            count += len(samples)
            self.last_sample_count = len(samples)
            limit = len(output_items[0]) - self.last_sample_count
        return count

    def start(self):
        if self.BLE:
            print("Error: Bluetooth Thread already running!")
            return False

        # Reset state
        importlib.reload(psylink.bluetooth)
        importlib.reload(psylink.protocol)

        BackendClass = list(psylink.bluetooth.BACKENDS.values())[0]
        self.BLE = BackendClass(self.ble_mac)
        self.BLE.connect()
        self.actual_channels = self.BLE_decoder.decode_channel_count(self.BLE.read_channels())
        self.BLE.thread_start()

        return True

    def stop(self):
        if self.BLE:
            self.BLE.disconnect()
            self.BLE.thread_stop()
            self.BLE = None
        return True
