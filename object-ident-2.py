import cv2

#thres = 0.45 # Threshold to detect object

classNames = []
classFile = "coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, draw=True, objects=[]):
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
                    cv2.rectangle(img,box,color=(255,107,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
                    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # ret,thresh = cv2.threshold(gray,50,255,0)
                    # contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    # print(len(contours))
                if(confidence>0.65):
                    cv2.rectangle(img,(1,1),(40,40),color=(0,0,0),thickness=-1)
                    cv2.putText(img,str(len(objectInfo)),(10,25),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    # print(type(len(objectInfo)))

    return img,objectInfo


if __name__ == "__main__":

    cap = cv2.VideoCapture(1)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)


    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.45,0.2, objects=['person'])
        # print(len(objectInfo),'= number =  ',objectInfo)
        # print(objectInfo)
        cv2.imshow("Output",img)
        cv2.waitKey(1)
