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

    cv2.imwrite(filename, image)
    upload_image(filename)


main()