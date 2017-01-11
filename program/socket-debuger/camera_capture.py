import cv2
videoCapture = cv2.VideoCapture('clocka.avi')
fps = videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)

size = (int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
v = cv2.VideoWriter('bb.avi', -1, fps, size)

print fps, size,'v->',v

success, frame = videoCapture.read()

while success:
    cv2.imshow('MyWindow', frame)
    cv2.waitKey(1000/int(fps))
    v.write(frame)
    success, frame = videoCapture.read()
