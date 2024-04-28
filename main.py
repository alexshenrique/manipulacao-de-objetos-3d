import cv2
from cvzone.HandTrackingModule import HandDetector
import socket


# Parametros
largura, altura = 1280, 720

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3,largura)
cap.set(4,altura)



# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Comunicação com Unity
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1",5052)

while True:
    # Capturar o frame com a webcam
    success, img = cap.read()

    # Mãos
    hands, img = detector.findHands(img)

    data = []
    # Valores de Marcações = (x,y,z) * 21
    if hands:
        # Capturando a primeira mão detectada
        hand = hands[0]

        # Capturando a lista de marcações
        lmList = hand['lmList']
       # print(lmList)
        for lm in lmList:
            data.extend([lm[0], altura - lm[1], lm[2]])
        # print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)


    img = cv2.resize(img,(0,0),None,0.5, 0.5)
    cv2.imshow("Imagem", img)
    cv2.waitKey(1)