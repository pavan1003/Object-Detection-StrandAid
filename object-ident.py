import cv2
import time
import requests
from flask import Flask, jsonify, render_template, Response, request

from cv2 import imwrite
#thres = 0.45 # Threshold to detect object

app = Flask(__name__)

classNames = []
# classFile = "/home/pi/Desktop/Object_Detection_Files/coco.names"
classFile = "coco.names"

with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

# configPath = "/home/pi/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
# weightsPath = "/home/pi/Desktop/Object_Detection_Files/frozen_inference_graph.pb"
configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, cap, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    currentFrame = 0
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    if confidence > 0.75:
                        path="StrandAid.jpg"
                        cv2.imwrite(path,img)

                        #Request to upload Data
                        url = "https://strandaid.azurewebsites.net/objects"

                        payload = {
                        'data': '''{
                            "imageBy": 5,
                            "lat": 25,
                            "long": 69,
                            "object": "person",
                            "time": "October 8, 2022 at 4:28:27 AM UTC+5:30"
                        }'''}

                        files = [
                        ('file', open(path, "rb"))
                        ]

                        response = requests.request(method="POST", url=url, data=payload, files=files)
                        time.sleep(2)
                        # currentFrame += fps * 3000
                        # cap.set(cv2.CAP_PROP_POS_FRAMES, currentFrame)

    return img,objectInfo

def getVideo():
    cap = cv2.VideoCapture(0)
    cap.set(3,1920)
    cap.set(4,1080)
    #cap.set(10,70)


    while True:
        success, img = cap.read()
        # result, objectInfo = getObjects(img,0.45,0.2)
        result, objectInfo = getObjects(img,0.45,0.2, cap,objects=['person'])
        #print(objectInfo)
        cv2.imshow("Output",img)
        cv2.waitKey(1)

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()


        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
 

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video', methods=['GET'])
def video():
    return Response(getVideo(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)