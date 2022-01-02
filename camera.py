import cv2
import numpy as np
import time

# 현재 촬영된 이미지 정보를 전역으로 관리(최근 캡쳐한 사진 저장용)
frame = ''
count = 200
now_img = ''

class Video(object):
  def __init__(self, type):
    self.video = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    if not self.video.isOpened():
      print('웹캠을 열 수 없습니다.')
      exit()
    self.type = type
    # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
  def __del__(self):
    print('웹캠을 release 합니다.')
    self.video.release()
    time.sleep(1)
  def get_frame(self):
    while True:
      global frame
      ret, frame = self.video.read()
      if not ret:
        return 'done'
      else:
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()

def get_now_frame():
  print(frame)
  ret, jpg = cv2.imencode('.jpg', frame)
  global count, now_img
  count = count + 1
  cv2.imwrite('./static/images/' + 'captured_pic' + str(count) +  '.jpg', frame)
  now_img = 'captured_pic' + str(count) + '.jpg'
  return 'captured_pic'+str(count)+'.jpg'
  # return jpg.tobytes()

def get_now_jpg():
  return now_img

def get_now_frame_for_detect():
  return frame