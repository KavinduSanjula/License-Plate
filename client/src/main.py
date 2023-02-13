import uuid
import requests
import cv2

def upload_image(filename):
    url = 'http://127.0.0.1:5000/submit-image'
    files = {'image-file': open(filename,'rb')}
    resp = requests.post(url, files=files)
    print(resp) #debug


def main():
    camera = cv2.VideoCapture(0)
    _, image = camera.read()
    id = str(uuid.uuid4())
    filename = f"processed_images/{id}.jpg"
    filename='images/plate.jpeg'
    # cv2.imwrite(filename, image)
    upload_image(filename)


import serial

port = serial.Serial('COM4',9600) #serial port and baud rate

while port.is_open:
    data = port.readline()
    msg = data.decode('utf-8')
    if msg.strip() == "Hello, World!":  #checking string
        main()