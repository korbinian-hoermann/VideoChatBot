import json

import requests
import base64
import cv2
import numpy as np


files=[
  ('file',
   ('Korbi.jpg',open(r'C:/Users/korbi/Documents/speaker_detection_api/app/data/known_faces/Korbi.jpg','rb'),
    'image/jpeg'))
]

# api-endpoint
URL = "http://127.0.0.1:8000/process_image"
# defining a params dict for the parameters to be sent to the API
# sending get request and saving the response as response object
r = requests.post(url = URL,files=files)
print(r.json())
# extracting data in json format
arr = np.asarray(json.loads(r.json()["image"])).astype(np.uint8)  # resp.json() if using Python requestsprint(arr.shape)
print(arr.shape)
cv2.imshow("result", arr)
cv2.waitKey(0)
