import cv2
from collections import deque
import datetime
import time
import os
import threading


class Camera(threading.Thread):
    def __init__(self, msg_q, camera_num):
        super(Camera, self).__init__()
        self.saved_once = False
        self.SAVED_SECONDS = 6
        self.SAVED_TIME = self.SAVED_SECONDS * 15
        self.__frame = 0
        self.pre_pic = deque(maxlen=self.SAVED_TIME)
        self.after_pic = deque(maxlen=self.SAVED_TIME)
        self.pic = []
        self.alive = threading.Event()
        self.alive.set()
        self.msg_q = msg_q
        self.cap = cv2.VideoCapture(camera_num)
        self.__close_camera = False
        self.__single_mode = True
        self.__seq_video_writer = None

    def run(self):
        while True:
            if not self.cap.isOpened():
                time.sleep(1)
            elif self.alive.isSet():
                ret, frame = self.cap.read()
                font = cv2.FONT_ITALIC
                time_now = str(datetime.datetime.now())[:-3]
                cv2.putText(frame, time_now, (10, 470), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('Live Image', frame)
                n = self.pic.__len__()
                if self.__single_mode == False:
                    self.__seq_video_writer.write(frame)
                if n >= self.SAVED_TIME:
                    self.pic.pop(0)
                self.pic.append(frame)
                self.__frame += 1
                button = cv2.waitKey(1)
                if button == ord('q') or self.__close_camera:
                    self.cap.release()
                    cv2.destroyAllWindows()
                elif button == ord('s'):
                    self.save(str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))) + ".avi")

    def save(self, path):
        if os.path.exists("../data/") != True:
            os.makedirs("../data/")
        if os.path.exists("../data/" + path) != True:
            os.makedirs("../data/" + path)
        video_path = "../data/" + path + "/" + path + ".avi"
        threading.Thread(target=self.__save_video, args=(video_path, self.__frame)).start()

    def __save_video(self, path, frame_c):
        while self.__frame - frame_c < self.SAVED_TIME / 2:
            pass
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        videoWriter = cv2.VideoWriter(path, fourcc, 15.0, (640, 480))
        for p in self.pic[-self.SAVED_TIME:]:
            videoWriter.write(p)
        videoWriter.release()

    def close(self):
        self.__close_camera = True

    def open_camera(self, camera_num):
        self.__close_camera = False
        self.cap = cv2.VideoCapture(camera_num)
        self.alive.set()

    def set_single_mode(self, single, path=''):
        self.__single_mode = single
        if single == False:
            if os.path.exists("../Data/") != True:
                os.makedirs("../Data/")
            if os.path.exists("../Data/" + path) != True:
                os.makedirs("../Data/" + path)
            video_path = "../Data/" + path + "/" + path + ".avi"
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            self.__seq_video_writer = cv2.VideoWriter(video_path, fourcc, 15.0, (640, 480))
        else:
            if self.__seq_video_writer:
                self.__seq_video_writer.release()


if __name__ == "__main__":
    ca = Camera()
    ca.start()
