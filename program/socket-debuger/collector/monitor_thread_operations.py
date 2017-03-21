# coding=utf-8
import datetime
import threading
import time

import serial
import socket
import csv_writer


class myThread(threading.Thread):
    def __init__(
            self,
            settings,
            data_q,
            active_q,
            error_q,
            msg_q,
            camera,
            device="uart",
            port_stopbits=serial.STOPBITS_ONE,
            port_parity=serial.PARITY_NONE,
            port_timeout=0.01
    ):
        super(myThread, self).__init__()
        self.type = device
        self.display_data_q = data_q
        self.error_q = error_q
        self.active_q = active_q
        self.alive = threading.Event()
        self.alive.set()
        self.__enable_record_data = True
        self.__uart_pause = False
        # self.data_quene = deque(maxlen=1000)
        self.data_busy = False
        self.msg_q = msg_q
        self.MAX_LEN = 25000
        self.accx_data_quene = []
        self.accy_data_quene = []
        self.accz_data_quene = []
        self.gyox_data_quene = []
        self.gyoy_data_quene = []
        self.gyoz_data_quene = []
        self.acc_scale_data_quene = []
        self.acc_fchoice_data_quene = []
        self.acc_dlpf_data_quene = []
        self.gyo_scale_data_quene = []
        self.gyo_fchoice_data_quene = []
        self.gyo_dlpf_data_quene = []
        self.time_stamp_quene = []
        self.camera = camera
        self.force_record_flag = 0
        self.__single_mode = True
        self.__seq_csv_path = ''
        self.__seq_start_time = 0
        if self.type == "uart":
            self.serial_settings = settings
            self.serial_settings["stopbits"] = port_stopbits
            self.serial_settings["parity"] = port_parity
            self.serial_settings["timeout"] = port_timeout
            self.uart = None
            self.creat_serial()
        else:
            self.server_ip = settings["server_ip"]
            self.port = settings["port"]
            self.connect()

    def get_MSB(self, bytes):
        x = bytes[0] << 8 | (bytes[1])

        if (x & (1 << 16 - 1)):
            x = x - (1 << 16)

        y = bytes[2] << 8 | (bytes[3])
        if (y & (1 << 16 - 1)):
            y = y - (1 << 16)

        z = bytes[4] << 8 | (bytes[5])
        if (z & (1 << 16 - 1)):
            z = z - (1 << 16)

        return x, y, z

    def pulse_max(self, data):
        def mean(data):
            return sum(data) / len(data)

        stable_value = mean(data[:5])
        max_value = 0
        for i in range(len(data)):
            max_value = max(max_value, abs(data[i] - stable_value))
        return max_value

    def run(self):
        coming_flag = 0
        start_time = 0
        csv_path = ""
        self.count = 0
        stable_count = 0

        self.frame_count = 0
        vehicle_coming_frame = 0
        while self.alive.isSet():
            if self.type == "uart":
                head = self.uart.read(1)
            else:
                head = self.client.recv(1)
            if head and ord(head) == 0x7D:
                if self.type == "uart":
                    head = self.uart.read(1)
                else:
                    head = self.client.recv(1)
                if head and ord(head) == 0x7E:
                    if self.type == "uart":
                        line = self.uart.read(18)
                    else:
                        line = self.client.recv(18)
                    data = []
                    for s in line:
                        data.append(ord(s))
                    if len(data) == 18:
                        self.count += 1
                        self.frame_count += 1
                        acc_x, acc_y, acc_z = self.get_MSB(data[:6])
                        gyo_x, gyo_y, gyo_z = self.get_MSB(data[6:])
                        if -32769 < acc_x < 32769 and -32769 < acc_y < 32769 and -32769 < acc_z < 32769 and \
                                                -32769 < gyo_x < 32769 and -32769 < gyo_y < 32769 and -32769 < gyo_z < 32769:

                            acc_scale = data[12]
                            acc_fchoice = data[13]
                            acc_dlpf = data[14]
                            gyo_scale = data[15]
                            gyo_fchoice = data[16]
                            gyo_dlpf = data[17]
                            timestamp = str(datetime.datetime.now())[:-3].replace(" ", "_")
                            self.display_data_q.put(([acc_x, acc_y, acc_z,
                                                      gyo_x, gyo_y, gyo_z,
                                                      acc_scale, acc_fchoice, acc_dlpf,
                                                      gyo_scale, gyo_fchoice, gyo_dlpf],
                                                     timestamp, self.frame_count))
                            n = self.acc_scale_data_quene.__len__()
                            if n >= self.MAX_LEN:
                                self.accx_data_quene.pop(0)
                                self.accy_data_quene.pop(0)
                                self.accz_data_quene.pop(0)
                                self.gyox_data_quene.pop(0)
                                self.gyoy_data_quene.pop(0)
                                self.gyoz_data_quene.pop(0)
                                self.acc_scale_data_quene.pop(0)
                                self.gyo_scale_data_quene.pop(0)
                                self.acc_fchoice_data_quene.pop(0)
                                self.acc_dlpf_data_quene.pop(0)
                                self.gyo_fchoice_data_quene.pop(0)
                                self.gyo_dlpf_data_quene.pop(0)
                                self.time_stamp_quene.pop(0)
                            self.accx_data_quene.append(acc_x)
                            self.accy_data_quene.append(acc_y)
                            self.accz_data_quene.append(acc_z)
                            self.gyox_data_quene.append(gyo_x)
                            self.gyoy_data_quene.append(gyo_y)
                            self.gyoz_data_quene.append(gyo_z)
                            self.acc_scale_data_quene.append(acc_scale)
                            self.acc_dlpf_data_quene.append(acc_dlpf)
                            self.acc_fchoice_data_quene.append(acc_fchoice)
                            self.gyo_dlpf_data_quene.append(gyo_dlpf)
                            self.gyo_fchoice_data_quene.append(gyo_fchoice)
                            self.gyo_scale_data_quene.append(gyo_scale)
                            self.time_stamp_quene.append(timestamp)
                            if n == 300:
                                self.msg_q.put("Data Quene Ready")
                            if self.__single_mode == True:
                                if n > 300:
                                    coming_pulse = self.pulse_max(self.accz_data_quene[n - 200:])
                                    if coming_flag == 0 and coming_pulse > 2000 or self.force_record_flag != 0:
                                        self.msg_q.put("Vehicle Coming")
                                        start_time = time.time()
                                        coming_flag = 1
                                        stable_count = 0
                                        csv_path = str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))
                                        vehicle_coming_frame = self.frame_count - 300
                                        if self.camera:
                                            self.camera.save(csv_path)
                                    if coming_flag == 1 and coming_pulse < 500:
                                        stable_count += 1
                                        if stable_count > 100:
                                            coming_flag = 0
                                            stable_count = 0
                                            self.msg_q.put("Vehicle Leaving, {} Seconds data saved".format(
                                                round(time.time() - start_time, 3) + 3.6
                                            ))
                                            data_dict = {}
                                            quene_range = -(self.frame_count - vehicle_coming_frame)
                                            data_dict['time'] = self.time_stamp_quene[quene_range:]
                                            data_dict['acc_x'] = self.accx_data_quene[quene_range:]
                                            data_dict['acc_y'] = self.accy_data_quene[quene_range:]
                                            data_dict['acc_z'] = self.accz_data_quene[quene_range:]
                                            data_dict['gyo_x'] = self.gyox_data_quene[quene_range:]
                                            data_dict['gyo_y'] = self.gyoy_data_quene[quene_range:]
                                            data_dict['gyo_z'] = self.gyoz_data_quene[quene_range:]
                                            data_dict['acc_scale'] = self.acc_scale_data_quene[quene_range:]
                                            data_dict['acc_fchoice'] = self.acc_fchoice_data_quene[quene_range:]
                                            data_dict['acc_dlpf'] = self.acc_dlpf_data_quene[quene_range:]
                                            data_dict['gyo_scale'] = self.gyo_scale_data_quene[quene_range:]
                                            data_dict['gyo_fchoice'] = self.gyo_fchoice_data_quene[quene_range:]
                                            data_dict['gyo_dlpf'] = self.gyo_dlpf_data_quene[quene_range:]

                                            self.active_q.put(data_dict)
                                            t = threading.Thread(target=self.save_data, args=(data_dict, csv_path))
                                            t.start()
                            else:
                                if self.frame_count % 100 == 0:
                                    data_dict = {}
                                    quene_range = -100
                                    data_dict['time'] = self.time_stamp_quene[quene_range:]
                                    data_dict['acc_x'] = self.accx_data_quene[quene_range:]
                                    data_dict['acc_y'] = self.accy_data_quene[quene_range:]
                                    data_dict['acc_z'] = self.accz_data_quene[quene_range:]
                                    data_dict['gyo_x'] = self.gyox_data_quene[quene_range:]
                                    data_dict['gyo_y'] = self.gyoy_data_quene[quene_range:]
                                    data_dict['gyo_z'] = self.gyoz_data_quene[quene_range:]
                                    data_dict['acc_scale'] = self.acc_scale_data_quene[quene_range:]
                                    data_dict['acc_fchoice'] = self.acc_fchoice_data_quene[quene_range:]
                                    data_dict['acc_dlpf'] = self.acc_dlpf_data_quene[quene_range:]
                                    data_dict['gyo_scale'] = self.gyo_scale_data_quene[quene_range:]
                                    data_dict['gyo_fchoice'] = self.gyo_fchoice_data_quene[quene_range:]
                                    data_dict['gyo_dlpf'] = self.gyo_dlpf_data_quene[quene_range:]
                                    if int(time.time()) - self.__seq_start_time > 2000:
                                        self.set_single_mode(True)
                                        self.set_single_mode(False)
                                    t = threading.Thread(target=self.save_data, args=(data_dict, self.__seq_csv_path))
                                    t.start()

    def creat_serial(self):
        try:
            if self.uart:
                self.uart.close()
            self.uart = serial.Serial(**self.serial_settings)
        except serial.SerialException as e:
            self.error_q.put(e.message)

    def connect(self):
        addr = (self.server_ip, int(self.port))
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(addr)

    def force_record(self):
        self.force_record_flag = 1

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)

    def send(self, data):
        if self.type == "uart":
            for v in data:
                self.uart.write(chr(v).encode("ISO-8859-1"))
        else:
            for v in data:
                self.client.send(chr(v).encode("ISO-8859-1"))

    def save_data(self, data, csv_path):
        # self.camera.save(csv_path)
        csv_writer.write(data, csv_path)

    def set_single_mode(self, single):
        self.__single_mode = single
        if single == False:
            self.__seq_csv_path = str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))
            self.camera.set_single_mode(False, self.__seq_csv_path)
            self.__seq_start_time = int(time.time())
        else:
            self.camera.set_single_mode(True)
