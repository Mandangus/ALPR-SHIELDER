from genericpath import exists
import cv2
import os
import numpy as np
import easyocr
import re


RTSP_CELULAR = "rtsp://192.168.0.10:5540/ch0"
RTSP_SHIELDER = "rtsp://admin:Intelbras1234%23@192.168.1.173/cam/realmonitor?channel=1&subtype=1"
def setup(rtsp):
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
    cap = cv2.VideoCapture(rtsp)
    if cap == None:
        return -1
    #carregando o modelo de reconhecimento de placa
    net = cv2.dnn.readNet("fvlpd-net.weights","fvlpd-net.cfg")
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416,416),scale=1/255)


    return cap,model,COLORS,class_names

def setup_img(image_filename):

    if exists("output.jpg"):
        os.remove("output.jpg")

    imagem = cv2.imread(image_filename)
    
    #carregando o modelo de reconhecimento de placa
    net = cv2.dnn.readNet("fvlpd-net.weights","fvlpd-net.cfg")
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416,416),scale=1/255)

    return imagem, model

def find_plate(image,model):
    frame = image
    #detectando uma possivel placa
    classes, scores, boxes = model.detect(frame,0.2,0.2)
    print(classes)
    for(_, _, box) in zip(classes,scores,boxes):   
        if not exists("output.jpg"):
            new_frame = frame[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
            cv2.imwrite("output.jpg",new_frame)
            return True 
    return False   


def capture(cap,model,COLORS,class_names):
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
        if saved_score > 0.79:
            break  
        cv2.imshow("detections",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def ocr():
    """
    Função de leitura ocr com easyocr, faz a leitura do arquivo output.jpg
    """
    leitor = easyocr.Reader(['en'],gpu=False)
    texto = leitor.readtext('output.jpg')
    return texto

def filtrar(entry):
    """
    Função para filtrar o output do easyocr
    pega uma entrada e transforma em uma tupla (string, float)
    """
    
    valor = []
    confianca = []
    flag1 = False
    flag2 = True
    entry = str(entry)
    for char in entry:
        if flag1 and char != '\'':
            valor.append(char)
        if char == '\'':
            flag1 = not flag1
    for char in entry[::-1]:
        if flag2 and char != ')':
            confianca.append(char)
        if char == '.':
            break
    confianca = confianca[::-1]
        
    return (''.join(valor),float(''.join(confianca)))

def print_results(texto):
    regex_brasil = r'[A-Za-z]{3}\s?[0-9][0-9A-Za-z][0-9]{2}'
    for entry in texto:
        pal = filtrar(entry)
        print(pal)
        if re.match(regex_brasil,pal[0]):
            print("Essa aqui --> " + pal[0])
        return pal


def main_image_procedure(image_path):
    imagem, model = setup_img(image_path)
    if find_plate(imagem,model):
        text = print_results(ocr())
    else:
        text = "placa não encontrada"
    return text

def main_procedure(rtsp):
    if rtsp == "":
        rtsp = RTSP_SHIELDER
    try:
        cap,model,COLORS,class_names = setup()
    except:
        return "ERRO NO SETUP"
    capture(cap,model,COLORS,class_names)
    out = ocr()
    print_results(out)



