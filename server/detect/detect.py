import torch
import cv2
import easyocr

from datetime import datetime


class Logger:

    @classmethod
    def log_to_output(cls, *msg):
        with open("output_log.txt",'a') as file:
            time_stamp = datetime.now().timestamp()
            message = " - ".join(msg)
            file.write(f"{time_stamp} : {message}\n")

    @classmethod
    def log_to_error(cls, *msg):
        with open("error_log.txt",'a') as file:
            time_stamp = datetime.now().timestamp()
            message = " - ".join(msg)
            file.write(f"[ERROR] : {time_stamp} : {message}\n")


class DetectorOutput:
    def __init__(self, image, data):
        self.image = image
        self.text_data = [text for text in data]

    def __repr__(self) -> str:
        return f'Detector Output - {self.text_data}'




class Detector:

    def __init__(self):
        #CRITICAL -- *.pt file path needs to be reletive to src 
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', 'detect/best.pt')  # custom trained model
        self.ocr = easyocr.Reader(['en'])

    def detect(self, image):
        output = self.__detect(image)
        return DetectorOutput(image,output)

    def __detect(self, image):

        tensor = self.model(image)
        arr = tensor.pandas().xyxy[0].to_numpy()

        for element in arr:
            minX, minY, maxX, maxY, conf, id, label = element
            x1,y1,x2,y2 = int(minX), int(minY), int(maxX), int(maxY)


            cv2.rectangle(image,(x1,y1), (x2,y2), (255,0,0),2)
            roi = image[y1:y2, x1:x2]

            result = self.ocr.readtext(roi)
            
            for list in result:
                text = str(list[-2])
                if len(text) >=3:
                    yield text

