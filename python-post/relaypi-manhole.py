# coding=utf-8
import time
import urllib2
import urllib
import serial
import threading
from collections import deque
import platform

__author__ = 'Changxiaodong'


class DataStruct:
    upload_data_quene = deque(maxlen=2)


class Relay:
    def __init__(self):
        self.data = DataStruct()

    def run(self):
        '''
        Parameter：

        Function：
                从串口接收到数据后上传至服务器
        Autor:xiaoxiami 2015.5.29
        Others：时间长会出错。可以修改，当数据与当前界面显示数据发生变化时在更新界面
        '''

        DATA_PACKET = 1
        DEBUG_PACKET = 2

        def initUartDependOnSystem():
            uart = serial.Serial()
            if platform.system() == "Linux":
                port = "/dev/ttyAMA0"
            else:
                port = "COM8"

            uart.port = port
            uart.baudrate = 115200
            uart.open()
            return uart

        def initLogDependOnSystem():
            import os
            if not os.path.exists("./Log/"):
                os.makedirs('./Log/')

            if platform.system() == "Linux":
                data_log_path = "./Log/" + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + '.txt'
            else:
                data_log_path = "./Log/" + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + '.txt'
            err_log_path = "./Log/log.txt"

            with open(err_log_path, "w") as f:
                f.write(
                    "Program Start at:" + time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())) + "\n")
            print "running"

            log = {}
            log["data_log"] = data_log_path
            log["err_log"] = err_log_path
            return log

        def writeErrlog(path, err):
            with open(path, "a") as f:
                f.write(str(err) + "\n")

        def getPacket():
            data = {}
            data["address"] = 0
            data["data_type"] = ""
            data["data"] = ""
            try:
                self.uart.read(14)
                data["address"] = ord(self.uart.read(1)) << 24 | ord(self.uart.read(1)) << 16 | \
                                  ord(self.uart.read(1)) << 8 | ord(self.uart.read(1))
                data["data_type"] = ord(self.uart.read(1))
                data["data"] = ord(self.uart.read(1)) << 8 | ord(self.uart.read(1))
            except serial.SerialException, err:
                writeErrlog(self.logpath["err_log"], err)
            return data

        def isPacketHead():
            try:
                head_str = self.uart.read(1)
            except serial.SerialException, err:
                writeErrlog(self.logpath["err_log"], err)
                return False
            if head_str != "":
                if ord(head_str) == 0x7E:
                    return True
            return False

        def clearUartInwaiting():
            self.uart.read(self.uart.inWaiting())

        def pushToUploadQuene(data):
            self.data.upload_data_quene.append(urllib.urlencode(data))

        self.uart = initUartDependOnSystem()
        self.logpath = initLogDependOnSystem()
        netUploadThread = threading.Thread(target=self.dataUpload)
        netUploadThread.setDaemon(True)
        netUploadThread.start()

        while 1:
            if isPacketHead():
                data = getPacket()
                print data
                pushToUploadQuene(data)
                clearUartInwaiting()

    def dataUpload(self):
        '''
        Parameter：

        Function：
                               将数据上传至服务器
        Autor:xiaoxiami 2015.12.3
        Others：
        '''

        def initNetlogFile(filename):
            with open(filename, "w") as f:
                f.write("running...")

        def postDataToServer(postdata):
            try:
                response = urllib2.urlopen("http://www.xiaoxiami.space/info/manhole-post/", post_data, timeout=2)
                feedback = eval(response.read())
                return feedback
            except urllib2.HTTPError, err:
                writeNetLog(net_log_filename, err)
                print err
            except urllib2.URLError, err:
                writeNetLog(net_log_filename, err)
                print err
            except:
                pass
            finally:
                while len(self.data.upload_data_quene) > 0:
                    self.data.upload_data_quene.pop()
            return ""

        def writeNetLog(filename, delay):
            try:
                if float(delay) > 1:
                    with open(filename, "a") as f:
                        f.write(str(delay) + "\n")
            except:
                with open(filename, "a") as f:
                    f.write(str(delay) + "\n")

        def isEmptyUploadbuf():
            return len(self.data.upload_data_quene)

        net_log_filename = "./Log/net_log.txt"
        initNetlogFile(net_log_filename)
        count = 0

        while True:
            if isEmptyUploadbuf() != 0:
                post_data = self.data.upload_data_quene.popleft()
                now = time.time()
                feedback = postDataToServer(post_data)
                print feedback
                receive = time.time()
                delay = receive - now
                writeNetLog(net_log_filename, delay)
            else:
                time.sleep(0.1)


if __name__ == '__main__':
    relay = Relay()
    relay.run()
