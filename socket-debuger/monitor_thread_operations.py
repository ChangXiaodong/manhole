import socket
import threading
import os
import time
from collections import deque
import serial

class myThread(threading.Thread):
    def __init__(
            self,
            settings,
            data_q,
            error_q,
            port_stopbits=serial.STOPBITS_ONE,
            port_parity=serial.PARITY_NONE,
            port_timeout=0.01
    ):
        super(myThread, self).__init__()
        self.serial_settings = settings
        self.serial_settings["stopbits"] = port_stopbits
        self.serial_settings["parity"] = port_parity
        self.serial_settings["timeout"] = port_timeout
        self.data_q = data_q
        self.error_q = error_q
        self.alive = threading.Event()
        self.alive.set()
        self.__enable_record_data = True
        self.__uart_pause = False
        self.data_quene = deque(maxlen=1000)
        self.data_busy = False
        self.value = deque(maxlen=1000)
        self.uart = None

    def get_MSB(self, bytes):
        x = bytes[0]<< 8 | (bytes[1] )

        if (x & (1 << 16 - 1)):
            x = x - (1 << 16)

        y = bytes[2] << 8 | (bytes[3])
        if (y & (1 << 16 - 1)):
            y = y - (1 << 16)

        z = bytes[4] << 8 | (bytes[5])
        if (z & (1 << 16 - 1)):
            z = z - (1 << 16)

        return {"x": x, "y": y, "z": z}

    def run(self):
        self.count = 0
        self.creat_serial()
        while self.alive.isSet():
            head = self.uart.read(1)
            if head and ord(head)==0x7D:
                head = self.uart.read(1)
                if head and ord(head) == 0x7E:
                    line = self.uart.read(12)
                    data = []
                    for s in line:
                        data.append(ord(s))
                    if len(data) == 12:
                        self.count += 1
                        acc = self.get_MSB(data[:6])
                        gyo = self.get_MSB(data[6:])
                        timestamp = time.time()
                        self.data_q.put(([acc['x'], acc['y'], acc['z'],
                                          gyo['x'], gyo['y'], gyo['z']],
                                         timestamp, self.count))
            #         else:
            #             print len(data)
            #     else:
            #         print "not 7E"
            # else:
            #     print "not 7D"

        if self.uart:
            self.uart.close()

    def creat_serial(self):
        try:
            if self.uart:
                self.uart.close()
            self.uart = serial.Serial(**self.serial_settings)
        except serial.SerialException, e:
            self.error_q.put(e.message)


    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)

