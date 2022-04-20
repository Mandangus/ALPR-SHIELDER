from genericpath import exists
import cv2
import os
import numpy as np
import easyocr

API_KEY = "K88780082388957"
RTSP_CELULAR = "rtsp://172.26.237.202:5540/ch0"
RTSP_SHIELDER = "rtsp://admin:Shielder1234@192.168.1.102:554/Streaming/Channels/102/"

padding = 10
if exists("output.jpg"):
    os.remove("output.jpg")

#cores para destacar o reconhecimento 
COLORS = [(0,255,255),(255,255,0)]

#nome das classes do reconhecimento da placa
class_names = []
p = os.path.realpath("fvlpd-names.txt")
with open(p, "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

#carregando a captura de video
cap = cv2.VideoCapture(RTSP_SHIELDER)

#carregando o modelo de reconhecimento de placa
net = cv2.dnn.readNet("fvlpd-net.weights","fvlpd-net.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416,416),scale=1/255)
saved_score = np.float32(0)

while True:
    #lendo os frames da captura
    _,frame = cap.read()

    #detectando uma possivel placa
    classes, scores, boxes = model.detect(frame,0.2,0.2)
    for(classid, score, box) in zip(classes,scores,boxes):
        
        if not exists("output.jpg") or score > saved_score:
            saved_score = np.float32(score)
            new_frame = frame[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
            cv2.imwrite("output.jpg",new_frame)
        
        #colocando n video a box de predição 
        color = COLORS[int(classid) % len(COLORS)]
        label = f"{class_names[classid]} : {score}"
        cv2.rectangle(frame,box,color,2)
        
        cv2.putText(frame,label,(box[0],box[1]-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)
        
    cv2.imshow("detections",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#Reconhecendo as letras com ocr agora

leitor = easyocr.Reader(['en'],gpu=False)
texto = leitor.readtext('output.jpg')
print(texto)
#TODO: melhorar reconhecimento das placas mercosul, resolver problema com conexão com cameras