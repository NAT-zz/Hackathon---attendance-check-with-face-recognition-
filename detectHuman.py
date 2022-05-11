import cv2
import numpy as np


protopath = "MobileNetSSD_deploy.prototxt"
modelpath = "MobileNetSSD_deploy.caffemodel"
detector = cv2.dnn.readNetFromCaffe(prototxt=protopath, caffeModel=modelpath)
#detector.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
#detector.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
DSIZE_FRAME=(1000,600)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]


maxCount = 0


def detect(frame,filterClass,rate):
    frame= cv2.resize(frame,DSIZE_FRAME)
    (H, W) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)

    detector.setInput(blob)
    person_detections = detector.forward()
    rects = []     
    for i in np.arange(0, person_detections.shape[2]):
        confidence = person_detections[0, 0, i, 2]
        if confidence > rate:
            idx = int(person_detections[0, 0, i, 1])
            if CLASSES[idx] not in filterClass: 
                continue
            person_box = person_detections[0, 0, i, 3:7] * np.array([W, H, W, H])
            rects.append(person_box)

    boundingboxes = np.array(rects)     # box hien tai
    boundingboxes = boundingboxes.astype(int)
    objects = boundingboxes
    count=0
    for bbox in objects:
        x1, y1, x2, y2 = bbox
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        
        crop_img = frame[y1:y2,x1:x2]
        count=count+1        
        #cv2.imwrite("video/output_sub"+str(count)+".png", crop_img)


        #text = "ID: {}".format(count)
        #cv2.putText(frame, text, (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
        
    opc_txt = "Count: {}".format(len(boundingboxes))
    cv2.putText(frame, opc_txt, (3, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
    
    global maxCount

    maxCount = maxCount if maxCount>len(boundingboxes) else len(boundingboxes)
    cv2.putText(frame, "max: "+str(maxCount), (3, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

    cv2.imshow('app',frame)
    return frame,count,maxCount



def detectByPathVideo(path, writer):
    count=0
    maxCount=0
    video = cv2.VideoCapture(path)
    check, frame = video.read()
    if check == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
        return
    while video.isOpened():
        #check is True if reading was successful 
        check, frame =  video.read()
        if check:
            frame,count,maxCount = detect(frame,['person'],0.5)
            if writer is not None:
                writer.write(frame)
            key = cv2.waitKey(1)
            if key== ord('q'):
                break
        else:
            break
    cv2.destroyAllWindows()
    video.release()
    writer.release()


if __name__ == "__main__":
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    out = cv2.VideoWriter("video/outputtest1.mp4", fourcc, 5.0, DSIZE_FRAME)
    detectByPathVideo('video/testvideo2.mp4',out)
    
    
