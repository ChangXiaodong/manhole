import cv2
from collections import deque
import datetime
import time
import os
import threading

class Camera(threading.Thread):
    def __init__(self, msg_q):
        super(Camera, self).__init__()
        self.saved_once = False
        self.SAVED_SECONDS = 6
        self.SAVED_TIME = self.SAVED_SECONDS * 15
        self.frame_count = 0
        self.pre_pic = deque(maxlen=self.SAVED_TIME)
        self.after_pic = deque(maxlen=self.SAVED_TIME)
        self.pic = []
        self.alive = threading.Event()
        self.alive.set()
        self.msg_q = msg_q

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened() and self.alive.isSet():
            ret, frame = self.cap.read()
            font = cv2.FONT_ITALIC
            time_now = str(datetime.datetime.now())[:-3]
            cv2.putText(frame, time_now, (10, 470), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Live Image', frame)
            n = self.pic.__len__()
            if n >= self.SAVED_TIME:
                self.pic.pop(0)
            self.pic.append(frame)
            self.frame_count += 1
            button = cv2.waitKey(1)
            if button == ord('q'):
                break
            elif button == ord('s'):
                self.save(str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))+".avi")
        self.cap.release()
        cv2.destroyAllWindows()

    def save(self, path):
        if os.path.exists("./data/") != True:
            os.makedirs("./data/")
        if os.path.exists("./data/" + path) != True:
            os.makedirs("./data/" + path)
        video_path = "./data/" + path + "/" + path + ".avi"
        threading.Thread(target=self.__save_video, args=(video_path, self.frame_count)).start()

    def __save_video(self, path, frame_count):
        while self.frame_count - frame_count < self.SAVED_TIME / 2:
            pass
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        videoWriter = cv2.VideoWriter(path, fourcc, 15.0, (640, 480))
        for p in self.pic[-self.SAVED_TIME:]:
            videoWriter.write(p)
        videoWriter.release()

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.alive.clear()
        threading.Thread.join(self, None)

if __name__ == "__main__":
    ca = Camera()
    ca.start()
