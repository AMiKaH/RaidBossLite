from flask import Flask
from datetime import datetime
import re
from flask import render_template
from flask import request
import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\peaceful-app-264902-aa6e0ccf949f.json'

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath("C:\\Users\\ameer\\OneDrive\\Desktop\\NWHacks\\AI Training\\8.jpg")

app = Flask(__name__)


@app.route('/form')
def my_form():
    return render_template('hello_there.html')

@app.route('/form', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text

@app.route('/test')
def getData():
    
    DBDictionary = {"ICYA H8N" : 'false',
                    "YSJAGAN" : 'true',
                    "399 KNF" : 'false',
                    "7UIN148" : 'true',
                    "EVS ROCK": 'true',
                    "WMY-9051": 'true'
                    }

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    objects = client.object_localization(image=image)

    #print(objects)

    response = client.text_detection(image=image)

    strAll = ''
    plate = "\n"

    #print(response.text_annotations[0])

    listText = response.text_annotations[0].description.split('\n')

    print (listText)
    print (type(listText))
    for text in listText: #response.text_annotations:
        
        strAll += "License plate number is: "
        plate += text
        #print (plate[0: len(plate) - 1])
        
        #print(text)
        #print(plate)
        #print(type(plate))

        if plate[0: len(plate) - 2].strip() in DBDictionary:
            return strAll + plate + (' Plate is valid' if DBDictionary[plate[0: len(plate) - 2].strip()] == 'false' else ' Plate is invalid')
        
        if plate[0: len(plate) - 1].strip()  in DBDictionary: 
            return strAll + plate + (' Plate is valid' if DBDictionary[plate[0: len(plate) - 1].strip()] == 'false' else ' Plate is invalid')

        if plate[0: len(plate)].strip()  in DBDictionary:
            return strAll + plate + (' Plate is valid' if DBDictionary[plate[0: len(plate)].strip()] == 'false' else ' Plate is invalid')

        #if plate[len(plate.strip()) - 1] == '\n':
        plate = ''
        strAll = ''

    return 'License plate not found in database'


@app.route("/")
def home():
    return "Hello, Flask2!"

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )