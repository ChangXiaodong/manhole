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
        self.SAVED_SECONDS = 3
        self.SAVED_TIME = self.SAVED_SECONDS * 24
        self.frame_count = 0
        self.frame_saved = 0
        self.pre_pic = deque(maxlen=self.SAVED_TIME)
        self.after_pic = deque(maxlen=self.SAVED_TIME)
        self.video_path = ""
        self.alive = threading.Event()
        self.alive.set()
        self.msg_q = msg_q

    def run(self):
        self.cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')

        while self.cap.isOpened() and self.alive.isSet():
            ret, frame = self.cap.read()
            font = cv2.FONT_ITALIC
            time_now = str(datetime.datetime.now())[:-3]
            cv2.putText(frame, time_now, (10, 470), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Live Image', frame)
            if self.saved_once == True:
                if self.frame_count > self.SAVED_TIME:
                    if self.frame_count < self.frame_saved + self.SAVED_TIME:
                        self.after_pic.append(frame)
                    else:
                        videoWriter = cv2.VideoWriter(self.video_path, fourcc, 24.0, (640, 480))
                        for i in xrange(self.SAVED_TIME):
                            videoWriter.write(self.pre_pic[i])
                        for i in xrange(self.SAVED_TIME):
                            videoWriter.write(self.after_pic[i])
                        videoWriter.release()
                        self.saved_once = False
                        self.msg_q.put("{} Seconds Video Saved".format(self.SAVED_SECONDS*2))
                else:
                    self.msg_q.put("video is shorter than {} seconds".format(self.SAVED_SECONDS))
                    self.saved_once = False
            else:
                self.pre_pic.append(frame)
            self.frame_count += 1
            button = cv2.waitKey(1)
            if button == ord('q'):
                break
            elif button == ord('s'):
                self.save(str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))+".avi")
        self.cap.release()
        cv2.destroyAllWindows()

    def save(self, path):
        self.saved_once = True
        self.frame_saved = self.frame_count
        if os.path.exists("./data/") != True:
            os.makedirs("./data/")
        if os.path.exists("./data/" + path) != True:
            os.makedirs("./data/" + path)
        self.video_path = "./data/" + path + "/" + path + ".avi"

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.alive.clear()
        threading.Thread.join(self, None)

if __name__ == "__main__":
    ca = Camera()
    ca.start()
