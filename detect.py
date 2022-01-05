import cv2
import numpy as np
from camera import *

### 현재 분류할 수 있는 클래스들과 모델리스트를 저장해놓음 ###
fish_classes = [['godeungeo'],['chamdom'],['gwangeo'],['wooruck']]
sushi_classes = [['doldom'],['jeonbok'],['yeoneo'],['bangeo']]
fish_model_list = ["models/fish/godeungeo.weights",
  "models/fish/chamdom.weights", "models/fish/gwangeo.weights","models/fish/wooruck.weights"]
sushi_model_list = ["models/sushi/doldom.weights", "models/sushi/jeonbok.weights", "models/sushi/yeoneo.weights",
"models/sushi/bangeo.weights"]
###########################################################


def detectModel(type):
  class_list = []
  model_list = []
  confidence_list = []
  # 캡쳐된 사진 가져오기
  frame = get_now_frame_for_detect()
  # type에 따라 class list를 바꿈
  if type == 'fish':
    class_list = fish_classes
    model_list = fish_model_list
    confidence_list = [0 for i in range(len(fish_classes))]
  else:
    class_list = sushi_classes
    model_list = sushi_model_list
    confidence_list = [0 for i in range(len(sushi_classes))]

  # 사진을 각각 모델에 적용하면서 만약 객체 인식이 되면 모델별로 confidence를 저장한다.
  for m in range(len(model_list)):
    net = cv2.dnn.readNet(model_list[m], "models/yolov4-obj.cfg")
    classes = class_list[m]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[l-1] for l in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    min_confidence = 0.5
    img = cv2.resize(frame,None,fx=1, fy=1)
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    print(class_ids, confidences, boxes)
    for out in outs:
      for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        # confidence가 0.5 이상이면 감지
        if confidence > min_confidence:
          # Object detected
          center_x = int(detection[0] * width)
          center_y = int(detection[1] * height)
          w = int(detection[2] * width)
          h = int(detection[3] * height)

          # Rectangle coordinates
          x = int(center_x - w / 2)
          y = int(center_y - h / 2)

          boxes.append([x, y, w, h])
          confidences.append(float(confidence))
          class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.4)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    fish = classes[0]
    confidence_list_temp = []
    # 이미지에 사각형 박스를 치고, label과 confidence를 박스 위에 표시
    for i in range(len(boxes)):
      if i in indexes:
        x, y, w, h = boxes[i]
        label = f"{fish} {confidences[i]:.2f}"
        print(label)
        confidence_list_temp.append(confidences[i] * 100)
        # confidence_list[m] = confidences[i] * 100
        color = colors[0]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
        cv2.rectangle(img, (x-1, y), (x + len(label) * 13 + 65, y - 25), color, -1)
        cv2.putText(img, label, (x, y - 8), font, 1, (0, 255, 0), 1)
    cv2.imwrite('./static/images/'+ type + '/' + fish + '_result_pic' + '.jpg', img)
    if len(confidence_list_temp) != 0:
      # print(confidence_list_temp)
      confidence_list[m] = max(confidence_list_temp)
      # print("confidence_list : ", confidence_list[m])
  # 가장 확률 높은 fish 찾기
  best_confidence = max(confidence_list)
  index = confidence_list.index(best_confidence)
  # 만약 가장 높은 confidence가 0일 경우 인식 실패
  if best_confidence == 0:
    final_fish = 'None'
    cv2.imwrite('./static/images/' + type + '/' + 'None' + '_result_pic' + '.jpg', frame)
  else:
    final_fish = class_list[index][0]
  return final_fish, int(best_confidence)
