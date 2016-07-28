import socket
import threading
import os
import time


class myThread(threading.Thread):
    def __init__(
            self,
            socket,
            status_bar,
            main_form,
            socket_type,
            acc_gen_data,
            gyo_gen_data,
            acc_update_label,
            gyo_update_lebal
    ):
        super(myThread, self).__init__()
        self.status_bar = status_bar
        self.link = socket.link
        self.socket = socket
        self.main_form = main_form
        self.socket_type = socket_type
        self.acc_gen_data = acc_gen_data
        self.gyo_gen_data = gyo_gen_data
        self.acc_update_label = acc_update_label
        self.gyo_update_lebal = gyo_update_lebal
        self.path = "Data/" + time.strftime(
            '%Y-%m-%d_%H-%M-%S',
            time.localtime(time.time())
        ) + '.txt'
        self.__enable_record_data = True
        self.initDataPath()

    def run(self):
        if self.socket_type == "TCP/Server":
            while 1:
                try:
                    conn, addr = self.link.accept()
                    break
                except OSError:
                    pass
            self.status_bar('Connected by {add}'.format(add=addr))
        elif self.socket_type == "TCP/Client":
            conn = self.link
            conn.settimeout(None)
            count = 0

            while 1:

                try:
                    data = conn.recv(14)
                except ConnectionAbortedError:
                    self.link.close()
                    print("Connection closed")
                    break
                except OSError:
                    self.link.close()
                    print("Connection closed")
                    break

                if len(data)>=14 and data[0] == 0x7D and data[1] == 0x7E:
                    acc_x = data[2] << 8 | data[3]
                    acc_y = data[4] << 8 | data[5]
                    acc_z = data[6] << 8 | data[7]
                    gyo_x = data[8] << 8 | data[9]
                    gyo_y = data[10] << 8 | data[11]
                    gyo_z = data[12] << 8 | data[13]
                    count += 1
                    self.acc_gen_data(acc_x, acc_y, acc_z, count)
                    self.gyo_gen_data(gyo_x, gyo_y, gyo_z, count)
                    self.acc_update_label(acc_x, acc_y, acc_z)
                    self.gyo_update_lebal(gyo_x, gyo_y, gyo_z)
                    if self.__enable_record_data:
                        with open(self.path, "a+") as file:
                            file.write(
                                time.strftime(
                                    '%Y-%m-%d %H:%M:%S ',
                                    time.localtime(time.time())
                                ) +
                                str(acc_x) + "|" +
                                str(acc_y) + "|" +
                                str(acc_z) + "|" +
                                str(gyo_x) + "|" +
                                str(gyo_y) + "|" +
                                str(gyo_z) + "|" +
                                str(time.time()) + "\n"
                            )
            self.main_form.open_pushButton.setEnabled(True)
            self.main_form.stop_pushButton.setEnabled(False)


    def initDataPath(self):
        if not os.path.exists("Data/"):
            os.makedirs("Data/")

    def setDataPath(self, path):
        self.path = "Data/" + path

    def enableRecordData(self, state):
        if state == True:
            self.__enable_record_data = True
        else:
            self.__enable_record_data = False


class Socket(object):
    def __init__(
            self,
            ip,
            port,
            type,
            main_form,
            acc_gen_data,
            gyo_gen_data,
            acc_update_label,
            gyo_update_lebal
    ):
        self.host_ip = ip
        self.port = port
        self.socket_type = type
        self.main_form = main_form
        self.statusbar = self.main_form.updateStatusBar
        self.acc_gen_data = acc_gen_data
        self.gyo_gen_data = gyo_gen_data
        self.acc_update_label = acc_update_label
        self.gyo_update_lebal = gyo_update_lebal

    def creat(self):
        if self.socket_type == "TCP/Server":
            self.link = self.creatSocketServer()
            status = "TCP/Server listening in {port}".format(port=self.port)
        elif self.socket_type == "TCP/Client":
            self.link = self.creatSocketClient()
            status = "TCP/Client connecting to {ip}:{port}".format(
                ip=self.host_ip, port=self.port
            )
        elif self.socket_type == "UDP/Server":
            status = "UDP/Server listening in {port}".format(port=self.port)
        elif self.socket_type == "UDP/Client":
            status = "UDP/Client connecting to {ip}:{port}".format(
                ip=self.host_ip, port=self.port
            )
        self.statusbar(status)
        self.receive_thread = myThread(
            self,
            self.statusbar,
            self.main_form,
            self.socket_type,
            self.acc_gen_data,
            self.gyo_gen_data,
            self.acc_update_label,
            self.gyo_update_lebal
        )
        self.receive_thread.setDaemon(True)
        self.receive_thread.start()

    def creatSocketServer(self):
        link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        link.bind((self.host_ip, int(self.port)))
        link.listen(1)
        return link

    def creatSocketClient(self):
        ip = self.host_ip
        port = self.port
        link = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        link.settimeout(2)
        link.connect((ip, int(port)))
        return link

    def close(self):
        self.link.close()

    def enableRecoedData(self, state):
        if state == True:
            self.receive_thread.enableRecordData(True)
        else:
            self.receive_thread.enableRecordData(False)

    def setDataPath(self, path):
        self.receive_thread.setDataPath(path)


def getIPAddress():
    return socket.gethostbyname(socket.getfqdn(socket.gethostname()))
