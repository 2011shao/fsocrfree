import io
import requests
from PIL import Image
from flask import Flask, request
from cnocr import CnOcr
import os

os.system('apt-get install -y libgl1-mesa-glx')
os.system('pip install onnxruntime')
os.system('pip install opencv-python-headless')

OCR_MODEL = CnOcr()
app = Flask(__name__)


@app.route('/')
def root():
  return {"message": "ocr!"}


@app.route('/ocr', methods=['GET', 'POST'])
def ocr():
  img_url = request.args.get('image_url')
  if img_url:
    if "http" in img_url:
      response = requests.get(img_url)
      if response.status_code == 200:
        img = Image.open(io.BytesIO(response.content))
        res = OCR_MODEL.ocr(img)
        textArr = ''
        for result in res:
          text = result['text']
          print('text', text)
          textArr = textArr + text
        print('dd', textArr)
        return textArr
      else:
        return 'image error'

    else:
      return 'url error'
  else:
    return 'no error'


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
