from google.cloud import datastore
from google.cloud import storage

import pytest
import requests
import six

import main
import subprocess
import os
import matplotlib.image
from PIL import Image
import io

#@pytest.fixture
def app():
    main.app.testing = True
    client = main.app.test_client()
    return client


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
    result = []
    for blob in blobs:
        result.append(blob)
        #result.append("https://storage.googleapis.com/approvedpepes/{}/".format(blob.name) )
    return result



def upload_photo(app,content,name):
    r = app.post(
        '/upload_photo',
        data={
            'file': (content, name)
        }
    )

    assert r.status_code == 302

def test_upload_photo(app,url,blob=None,path=None):
    if(blob):
        test_photo_data = blob
    elif(path):
        test_photo_data = read_img = matplotlib.image.imread(path)
    else:
        test_photo_data = requests.get(url).content
    r = app.post(
        '/upload_photo',
        data={
            'file': (six.BytesIO(test_photo_data), 'flertrtrrerex_and_vision.jpg')
        }
    )

    assert r.status_code == 302

def insertApprovedPepes():
    appe = app()
    for blob in list_blobs_with_prefix('approvedpepes',""):
        content = six.BytesIO(blob.download_as_string())
        #subprocess.call("gsutil mv gs://approvedpepes/{0} gs://pepes/".format(blob.name), shell=True)
        link =""        
        upload_photo(appe,content,'TestApproved.jpg')
        #print("hi")  test_photo_data = requests.get(url).content

def insertFromFolder(path):
    appe = app()
    for item in os.listdir(path):  
        try:
            img = Image.open(path+item, mode='r')
            imgByteArr = io.BytesIO()
            img.save(imgByteArr, format='PNG')
            imgByteArr = imgByteArr.getvalue() 
            img = six.BytesIO(imgByteArr)
            upload_photo(appe,img,item)
        except Exception as e:
            print(e)
