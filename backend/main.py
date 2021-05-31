import csv
import os
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import PIL.Image

## Global variable
model = None  #model
db = None
image_path = ""
tgl = ""
f_name = ""
value = ""

# Download model file from cloud storage bucket
def download_model_file():

    from google.cloud import storage

    # Model Bucket details
    BUCKET_NAME        = "team_b21"
    PROJECT_ID         = "adept-figure-313804"
    GCS_MODEL_FILE     = "model.h5"

    # Initialise a client
    client   = storage.Client(PROJECT_ID)
    
    # Create a bucket object for our bucket
    bucket   = client.get_bucket(BUCKET_NAME)
    
    # Create a blob object from the filepath
    blob     = bucket.blob(GCS_MODEL_FILE)
    
    folder = '/tmp/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Download the file to a destination
    blob.download_to_filename(folder + "model.h5")

def download_image(event, context):

    from google.cloud import storage

    file = event
    # Model Bucket details
    BUCKET_NAME        = "adept-figure-313804.appspot.com"
    PROJECT_ID         = "adept-figure-313804"
    GCS_IMAGE_FILE     = file['name']

    # Initialise a client
    client   = storage.Client(PROJECT_ID)
    
    # Create a bucket object for our bucket
    bucket   = client.get_bucket(BUCKET_NAME)
    
    # Create a blob object from the filepath
    blob     = bucket.blob(GCS_IMAGE_FILE)
    
    folder = '/tmp/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Download the file to a destination
    global image_path
    image_path = folder + GCS_IMAGE_FILE
    blob.download_to_filename(image_path)

    #adding function split name
    global f_name
    global tgl
    f_name = file['name']
    tgl = f_name.split('_') #use tgl[-2]


def cutix(event, context):
    
    #download image to predict
    download_image(event, context)

    #stop when wrong file uploaded
    if '.jpg' or '.jpeg' or '.png' not in f_name:
        return 0

    #deploy model locally
    global model
    if not model:
        download_model_file()
        model = tf.keras.models.load_model('/tmp/model.h5')
    
    
    #initialize firestore
    global db
    if not db:
        # Use the application default credentials
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': 'adept-figure-313804',
        })
    
    db = firestore.client()

    #image process
    img = image.load_img(image_path, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)


    #predict
    images = np.vstack([x])
    classes = model.predict(images, batch_size=10)
    cancer_class = np.argmax(classes)

    global value

    if cancer_class == 0:
        value = 'Penyakit yang anda alami diprediksi adalah Kanker Kulit yang termasuk dalam kelas (jenis) akiec'

    elif cancer_class == 1:
        value = 'Penyakit yang anda alami diprediksi adalah Kanker Kulit yang termasuk dalam kelas (jenis) bcc'

    elif cancer_class == 2:
        value = 'Penyakit yang anda alami diprediksi adalah Kanker Kulit yang termasuk dalam kelas (jenis) bkl'

    elif cancer_class == 3:
        value = 'Penyakit yang anda alami diprediksi adalah Kanker Kulit yang termasuk dalam kelas (jenis) df'

    elif cancer_class == 4:
        value = 'Penyakit yang anda alami diprediksi adalah Kanker Kulit yang termasuk dalam kelas (jenis) mel'

    elif cancer_class == 5:
        value = 'Penyakit yang anda alami diprediksi adalah Kanker Kulit yang termasuk dalam kelas (jenis) nv'

    elif cancer_class == 6:
        value = 'Penyakit yang anda alami diprediksi adalah Kanker Kulit yang termasuk dalam kelas (jenis) vasc'


    #update firestore
    doc_ref = db.collection(u'skin-cancer-classification').document(tgl[-2])
    doc_ref.set({
        f_name.strip('.jpg').strip('.jpeg').strip('.png'): value
    }, merge=True)
    print(f_name + '\n')
    print(tgl[-2] + '\n')
    print(value + '\n')
