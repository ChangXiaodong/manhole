import threading

class myThread(threading.Thread):
    def __init__(self):
        super(myThread, self).__init__()

    def run(self):
        print
        'start loop', self.nloop, 'at:', ctime()
        sleep(self.nsec)
        print
        'loop', self.nloop, 'done at:', ctime()