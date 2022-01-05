from flask import Flask, render_template, request, Response, redirect, url_for
from camera import *
from detect import *
from keras.models import load_model
from keras.preprocessing import image
from detect import *

import json
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/main')
def main():
  return render_template('main.html')
  
@app.route('/fish')
def fish():
  return render_template('fish.html')
def gen(camera, type):
  if type == 'video':
    print('녹화를 시작합니다.')
    while True:
      frame = camera.get_frame()
      if frame == 'done':
        break
      yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
  elif type == 'capture':
    print('capture를 시작합니다.')
    frame = camera.get_frame()
    yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/sushi')
def sushi():
  return render_template('sushi.html')
def gen(camera, type):
  if type == 'video':
    print('녹화를 시작합니다.')
    while True:
      frame = camera.get_frame()
      if frame == 'done':
        break
      yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')      
  elif type == 'capture':
    print('capture를 시작합니다.')
    frame = camera.get_frame()
    yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
  return Response(gen(Video(type='video'), 'video'),
  mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
  return get_now_frame()

@app.route('/result/fish')
def result_fish():
  fish, prediction = detectModel('fish')
  ### 해당 어종 페이지로 접근하기 ###
  # fish = 'cham'
  ### 
  # ret, jpg = cv2.imencode('.jpg', result)
  # cv2.imwrite('./static/images/fish/' + fish + '_result_pic' + '.jpg', result)
  print(fish)
  # 해당 어종에 대한 정보 불러오기
  with open('fish_data.json', 'r', encoding='UTF-8') as fish_data:
    data = json.load(fish_data)
    detail_info = {}
    for i in range(len(data)):
      if data[i]['id'] == fish:
        detail_info = data[i]
    
  return render_template('result_fish.html', fish = fish, detail = detail_info, prediction = prediction)

@app.route('/result/sushi')
def result_sushi():
  fish, prediction = detectModel('sushi')
  print(fish)
  ###
  # fish = 'gwangeo'
  ###

  # 해당 어종에 대한 정보 불러오기
  with open('fish_data.json', 'r', encoding='UTF-8') as fish_data:
    data = json.load(fish_data)
    detail_info = {}
    for i in range(len(data)):
      if data[i]['id'] == fish:
        detail_info = data[i]
  return render_template('result_sushi.html', fish = fish, detail = detail_info, prediction = prediction)
if __name__ == '__main__':
  app.run(debug=True)