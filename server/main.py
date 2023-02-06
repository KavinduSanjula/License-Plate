import os
import cv2
import queue
from datetime import datetime
from flask import Flask, request, redirect, flash, render_template
from threading import Thread
from detect import detect
import mysql.connector



UPLOAD_FOLDER = 'upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def save_data(filename, data):

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="license-plate"
    )
    cursor = mydb.cursor()
    time_stamp = datetime.now().timestamp()
    sql = f"INSERT INTO plate(timestamp,image,plate) VALUES('{time_stamp}','{filename}','{', '.join(data)}')"
    cursor.execute(sql)



class NumberPlateDetector(Thread):
    def __init__(self, image_queue):
        super().__init__()

        self.image_queue = image_queue
        self.detector = detect.Detector()

    def run(self):
        super().run()

        while True:
            print('BG Thread: running')
            filename = self.image_queue.get()
            image = cv2.imread(filename)
            out = self.detector.detect(image)
            save_data(filename, out.text_data)




UPLOAD_FOLDER = 'upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
image_queue = queue.Queue(maxsize=100)


@app.route('/', methods=['GET'])
def index():
    return  render_template('index.html')


@app.route('/submit-image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image-file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['image-file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(save_path)    #save uploaded file
        image_queue.put(save_path)  #submit to the image queue for detect plates

    return render_template('upload.html')



if __name__ == '__main__':
    
    # make detector as separate thread
    detector_thread = NumberPlateDetector(image_queue)
    detector_thread.start()

    app.run()

    detector_thread.join()
    