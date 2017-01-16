import Queue
import platform
YMAX = 10000.000
YMIN = -10000.000

DEFAULT_SCALE = 500
if platform.system() == "Darwin":
    data_file_path = "/Users/xiaoxiami/Manhole/test data/1-13/"
else:
    data_file_path = "E:/Manhole/test data/sorted data/bad manhole1/"



class LiveDataFeed(object):
    def __init__(self):
        self.cur_data = None
        self.has_new_data = False

    def add_data(self, data):
        self.cur_data = data
        self.has_new_data = True

    def read_data(self):
        self.has_new_data = False
        return self.cur_data

def get_all_from_queue(Q):
    """ Generator to yield one after the others all items
        currently in the queue Q, without any waiting.
    """
    try:
        while True:
            yield Q.get_nowait( )
    except Queue.Empty:
        raise StopIteration


def get_item_from_queue(Q, timeout=0.01):
    """ Attempts to retrieve an item from the queue Q. If Q is
        empty, None is returned.

        Blocks for 'timeout' seconds in case the queue is empty,
        so don't use this method for speedy retrieval of multiple
        items (use get_all_from_queue for that).
    """
    try:
        item = Q.get(True, 0.01)
    except Queue.Empty:
        return None
    return item

def enumerate_serial_ports():
    """
    Purpose:        scan for available serial ports
    Return:         return a list of of the availables ports names
    """
    import itertools
    portList = []
    import _winreg as winreg
    path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError:
        print "no avaliable uart"
        return
        # raise self.IterationError
    for i in itertools.count():
        try:
            val = winreg.EnumValue(key, i)
            portList.append(val)
        except EnvironmentError:
            break

    winreg.CloseKey(key)
    port = []
    for p in portList:
        port.append(str(p[1]))
    return port