# coding=utf-8
import datetime
import threading
import time

import serial
import socket
import csv_writer
import matplotlib.pyplot as plt


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
        # split data params
        WIDTH = 2
        MAX_CNT = 600
        start_flag = 0
        count = MAX_CNT
        stable_cnt = 0
        end_flag = 0
        acc_x_quene = []
        acc_y_quene = []
        acc_z_quene = []
        gyo_x_quene = []
        gyo_y_quene = []
        gyo_z_quene = []
        time_stamp_quene = []
        acc_scale_quene = []
        acc_fchoice_quene = []
        acc_dlpf_quene = []
        gyo_scale_quene = []
        gyo_fchoice_quene = []
        gyo_dlpf_quene = []

        pre_acc_x_quene = []
        pre_acc_y_quene = []
        pre_acc_z_quene = []
        pre_gyo_x_quene = []
        pre_gyo_y_quene = []
        pre_gyo_z_quene = []
        pre_time_stamp_quene = []
        pre_acc_scale_quene = []
        pre_acc_fchoice_quene = []
        pre_acc_dlpf_quene = []
        pre_gyo_scale_quene = []
        pre_gyo_fchoice_quene = []
        pre_gyo_dlpf_quene = []
        pivot_quene = []

        start_time = 0
        csv_path = ""
        self.frame_count = 0
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
                            pivot_value = acc_z
                            pivot_quene.append(pivot_value)
                            pre_acc_x_quene.append(acc_x)
                            pre_acc_y_quene.append(acc_y)
                            pre_acc_z_quene.append(acc_z)
                            pre_gyo_x_quene.append(gyo_x)
                            pre_gyo_y_quene.append(gyo_y)
                            pre_gyo_z_quene.append(gyo_z)
                            pre_acc_scale_quene.append(acc_scale)
                            pre_acc_dlpf_quene.append(acc_dlpf)
                            pre_acc_fchoice_quene.append(acc_fchoice)
                            pre_gyo_dlpf_quene.append(gyo_dlpf)
                            pre_gyo_fchoice_quene.append(gyo_fchoice)
                            pre_gyo_scale_quene.append(gyo_scale)
                            pre_time_stamp_quene.append(timestamp)

                            if pre_acc_scale_quene.__len__() > 100:
                                pre_acc_x_quene.pop(0)
                                pre_acc_y_quene.pop(0)
                                pre_acc_z_quene.pop(0)
                                pre_gyo_x_quene.pop(0)
                                pre_gyo_y_quene.pop(0)
                                pre_gyo_z_quene.pop(0)
                                pre_acc_scale_quene.pop(0)
                                pre_acc_dlpf_quene.pop(0)
                                pre_acc_fchoice_quene.pop(0)
                                pre_gyo_dlpf_quene.pop(0)
                                pre_gyo_fchoice_quene.pop(0)
                                pre_gyo_scale_quene.pop(0)
                                pre_time_stamp_quene.pop(0)
                                pivot_quene.pop(0)

                            if self.__single_mode == True:
                                if pivot_quene.__len__() > WIDTH + 1:
                                    slop = abs((pivot_quene[-1] - pivot_quene[-WIDTH]) / (WIDTH + 1))
                                    if start_flag == 0 and slop > 400:
                                        acc_x_quene = pre_acc_x_quene[:]
                                        acc_y_quene = pre_acc_y_quene[:]
                                        acc_z_quene = pre_acc_z_quene[:]
                                        gyo_x_quene = pre_gyo_x_quene[:]
                                        gyo_y_quene = pre_gyo_y_quene[:]
                                        gyo_z_quene = pre_gyo_z_quene[:]
                                        time_stamp_quene = pre_time_stamp_quene[:]
                                        acc_scale_quene = pre_acc_scale_quene[:]
                                        acc_fchoice_quene = pre_acc_fchoice_quene[:]
                                        acc_dlpf_quene = pre_acc_dlpf_quene[:]
                                        gyo_scale_quene = pre_gyo_scale_quene[:]
                                        gyo_fchoice_quene = pre_gyo_fchoice_quene[:]
                                        gyo_dlpf_quene = pre_gyo_dlpf_quene[:]

                                        count = MAX_CNT
                                        stable_cnt = 0
                                        start_flag = 1
                                        self.msg_q.put("Vehicle Coming")
                                        start_time = time.time()
                                        csv_path = str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))
                                        if self.camera:
                                            self.camera.save(csv_path)
                                    if start_flag == 1:
                                        acc_x_quene.append(acc_x)
                                        acc_y_quene.append(acc_y)
                                        acc_z_quene.append(acc_z)
                                        gyo_x_quene.append(gyo_x)
                                        gyo_y_quene.append(gyo_y)
                                        gyo_z_quene.append(gyo_z)
                                        acc_scale_quene.append(acc_scale)
                                        acc_dlpf_quene.append(acc_dlpf)
                                        acc_fchoice_quene.append(acc_fchoice)
                                        gyo_dlpf_quene.append(gyo_dlpf)
                                        gyo_fchoice_quene.append(gyo_fchoice)
                                        gyo_scale_quene.append(gyo_scale)
                                        time_stamp_quene.append(timestamp)

                                        count -= 1
                                        if count == 0:
                                            print("count")
                                            end_flag = 1
                                        if slop < 400:
                                            stable_cnt += 1
                                        else:
                                            stable_cnt = 0
                                        if stable_cnt > 200:
                                            if count < MAX_CNT // 2:
                                                print("stable")
                                                end_flag = 1

                                    if end_flag == 1:
                                        start_flag = 0
                                        end_flag = 0
                                        count = MAX_CNT
                                        stable_cnt = 0
                                        self.msg_q.put("Vehicle Leaving, {} Seconds data saved".format(
                                            round(time.time() - start_time, 3)
                                        ))

                                        data_dict = {}
                                        data_dict['time'] = time_stamp_quene[:]
                                        data_dict['acc_x'] = acc_x_quene[:]
                                        data_dict['acc_y'] = acc_y_quene[:]
                                        data_dict['acc_z'] = acc_z_quene[:]
                                        data_dict['gyo_x'] = gyo_x_quene[:]
                                        data_dict['gyo_y'] = gyo_y_quene[:]
                                        data_dict['gyo_z'] = gyo_z_quene[:]
                                        data_dict['acc_scale'] = acc_scale_quene
                                        data_dict['acc_fchoice'] = acc_fchoice_quene
                                        data_dict['acc_dlpf'] = acc_dlpf_quene
                                        data_dict['gyo_scale'] = gyo_scale_quene
                                        data_dict['gyo_fchoice'] = gyo_fchoice_quene
                                        data_dict['gyo_dlpf'] = gyo_dlpf_quene
                                        self.active_q.put(data_dict)
                                        t = threading.Thread(target=self.save_data, args=(data_dict, csv_path))
                                        t.start()
                                        pre_acc_x_quene = []
                                        pre_acc_y_quene = []
                                        pre_acc_z_quene = []
                                        pre_gyo_x_quene = []
                                        pre_gyo_y_quene = []
                                        pre_gyo_z_quene = []
                                        pre_time_stamp_quene = []
                                        pre_acc_scale_quene = []
                                        pre_acc_fchoice_quene = []
                                        pre_acc_dlpf_quene = []
                                        pre_gyo_scale_quene = []
                                        pre_gyo_fchoice_quene = []
                                        pre_gyo_dlpf_quene = []
                                        acc_x_quene = []
                                        acc_y_quene = []
                                        acc_z_quene = []
                                        gyo_x_quene = []
                                        gyo_y_quene = []
                                        gyo_z_quene = []
                                        time_stamp_quene = []
                                        acc_scale_quene = []
                                        acc_fchoice_quene = []
                                        acc_dlpf_quene = []
                                        gyo_scale_quene = []
                                        gyo_fchoice_quene = []
                                        gyo_dlpf_quene = []
                            else:
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


class staticThread(threading.Thread):
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
        super(staticThread, self).__init__()
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
        self.serial_settings = settings
        self.serial_settings["stopbits"] = port_stopbits
        self.serial_settings["parity"] = port_parity
        self.serial_settings["timeout"] = port_timeout
        self.uart = None
        self.creat_serial()


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
        # split data params
        acc_x_quene = []
        acc_y_quene = []
        acc_z_quene = []
        gyo_x_quene = []
        gyo_y_quene = []
        gyo_z_quene = []
        var_quene = []

        self.frame_count = 0
        while self.alive.isSet():
            head = self.uart.read(1)
            if head and ord(head) == 0x0D:
                head = self.uart.read(1)
                if head and ord(head) == 0x0A:
                    buf = self.uart.read(10)
                    max_index = []
                    max_index.append(ord(buf[0]) << 8 | ord(buf[1]))
                    max_index.append(ord(buf[2]) << 8 | ord(buf[3]))
                    max_index.append(ord(buf[4]) << 8 | ord(buf[5]))
                    max_index.append(ord(buf[6]) << 8 | ord(buf[7]))
                    max_index.append(ord(buf[8]) << 8 | ord(buf[9]))

                    buf = self.uart.read(10)
                    min_index = []
                    min_index.append(ord(buf[0]) << 8 | ord(buf[1]))
                    min_index.append(ord(buf[2]) << 8 | ord(buf[3]))
                    min_index.append(ord(buf[4]) << 8 | ord(buf[5]))
                    min_index.append(ord(buf[6]) << 8 | ord(buf[7]))
                    min_index.append(ord(buf[8]) << 8 | ord(buf[9]))


                    fig = plt.figure()
                    ax = fig.add_subplot(211)
                    ax.plot(acc_x_quene)
                    ax.plot(acc_y_quene)
                    ax.plot(acc_z_quene)
                    print(max_index)
                    print(min_index)
                    for i in range(len(max_index)):
                        if max_index[i] * min_index[i] != 0:
                            ax.plot(max_index[i], acc_z_quene[0], 'ro')
                            ax.plot(min_index[i], acc_z_quene[0], 'go')
                    ax = fig.add_subplot(212)

                    ax.plot(var_quene)
                    plt.show()
                    acc_x_quene = []
                    acc_y_quene = []
                    acc_z_quene = []
                    gyo_x_quene = []
                    gyo_y_quene = []
                    gyo_z_quene = []
                    var_quene = []

            if head and ord(head) == 0x7D:
                head = self.uart.read(1)
                if head and ord(head) == 0x7E:
                    line = self.uart.read(16)
                    data = []
                    for s in line:
                        data.append(ord(s))
                    if len(data) == 16:
                        self.frame_count += 1
                        acc_x, acc_y, acc_z = self.get_MSB(data[:6])
                        gyo_x, gyo_y, gyo_z = self.get_MSB(data[6:])
                        if -32769 < acc_x < 32769 and -32769 < acc_y < 32769 and -32769 < acc_z < 32769 and \
                                                -32769 < gyo_x < 32769 and -32769 < gyo_y < 32769 and -32769 < gyo_z < 32769:
                            acc_x_quene.append(acc_x)
                            acc_y_quene.append(acc_y)
                            acc_z_quene.append(acc_z)
                            gyo_x_quene.append(gyo_x)
                            gyo_y_quene.append(gyo_y)
                            gyo_z_quene.append(gyo_z)

                            var = data[12] << 24 | data[13] << 16 | data[14] << 8 | data[15]
                            var_quene.append(var)

    def creat_serial(self):
        try:
            if self.uart:
                self.uart.close()
            self.uart = serial.Serial(**self.serial_settings)
        except serial.SerialException as e:
            self.error_q.put(e.message)
