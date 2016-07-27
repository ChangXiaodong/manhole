import socket
import threading

class myThread(threading.Thread):
    def __init__(self, link, status_bar, main_form):
        super(myThread, self).__init__()
        self.status_bar = status_bar
        self.link = link
        self.main_form = main_form

    def run(self):
        while 1:
            try:
                conn, addr = self.link.accept()
                break
            except OSError:
                pass
        self.status_bar('Connected by {add}'.format(add=addr))
        while 1:
            try:
                data = conn.recv(16)
                if not data:
                    raise ConnectionResetError
            except ConnectionResetError:
                self.status_bar("Connection closed by client")
                self.main_form.open_pushButton.setEnabled(True)
                self.main_form.stop_pushButton.setEnabled(False)
                self.link.close()
                return
            print(data)



class Socket(object):
    def __init__(self, ip, port, type, status, main_form):
        self.host_ip = ip
        self.listen_port = port
        self.socket_type = type
        self.main_form = main_form
        self.statusbar = self.main_form.updateStatusBar

    def creat(self):
        if self.socket_type == "TCP/Server":
            self.link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.link.bind((self.host_ip, int(self.listen_port)))
            self.link.listen(1)
            status="TCP/Server listening in {port}".format(port=self.listen_port)
        elif self.socket_type == "TCP/Client":
            status = "TCP/Client connecting to {ip}:{port}".format(
                ip=self.host_ip,port=self.listen_port
            )
        elif self.socket_type == "UDP/Server":
            status = "UDP/Server listening in {port}".format(port=self.listen_port)
        elif self.socket_type == "UDP/Client":
            status = "UDP/Client connecting to {ip}:{port}".format(
                ip=self.host_ip,port=self.listen_port
            )
        self.statusbar(status)
        receive_thread = myThread(self.link, self.statusbar, self.main_form)
        receive_thread.setDaemon(True)
        receive_thread.start()


        # while 1:
        #     conn, addr = self.link.accept()
        #     self.status_bar('Connected by {add}'.format(add=addr))
        #     while 1:
        #         data = conn.recv(10)
        #         print(data)
        #ConnectionResetError


    def close(self):
        self.link.close()

def getIPAddress():
    return socket.gethostbyname(socket.getfqdn(socket.gethostname()))
