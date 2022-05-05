import base64
import cv2
import time
import requests


def main():
    apipath = "http://127.0.0.1:5000/alpr"
    image_name = "output.jpg"
    try:
        cap = cv2.VideoCapture("rtsp://admin:Intelbras1234%23@192.168.1.173/cam/realmonitor?channel=1&subtype=1")
    except cv2.error as e:
        print("Erro na leitura da camera")
        return

    interval = 2

    settime = time.time()
    while True:
        _,frame = cap.read()
        if time.time() >= settime + interval:
            print("tempo que foi tirada a foto: " + str(time.time()))
            cv2.imwrite(image_name,frame)
            try:
                with open(image_name, "rb") as img_file:
                    encoded_image = base64.b64encode(img_file.read())
                    encoded_image = encoded_image.decode('utf-8')
                    encoded_image = "data:image/jpeg;base64," + encoded_image
            except Exception as e:
                print("ERRO NO ENCODING DA IMAGEM PELO CLIENTE")
                return
            settime = time.time()
            data = encoded_image
            r = requests.post(apipath,data=data)
            print(r.content.decode('utf-8'))


if __name__ == '__main__':
    main()