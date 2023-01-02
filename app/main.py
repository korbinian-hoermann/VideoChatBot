import json
import time

from fastapi import FastAPI, File, HTTPException
import face_recognition
import uvicorn
from pydantic import BaseModel
import numpy as np
import base64
import cv2
import io

from PIL import Image
from components.image_preprocessing import preprocess_image

def decode_image(imageData) -> np.ndarray:
    header, imageData = imageData.split(",")[0], imageData.split(",")[1]
    image = np.array(Image.open(io.BytesIO(base64.b64decode(imageData))))
    image = cv2.cvtColor(src=image, code=cv2.COLOR_BGRA2RGB)
    return header, image

app = FastAPI()


@app.get('/')
def index():
    return {'message': 'Hello, World'}

@app.post("/process_image")
def process_image(file: bytes = File(...)):
    print("processing frame image")
    try:
        image = np.array(Image.open(io.BytesIO(file)))
        # Convert the image from BGR color to RGB color (which face_recognition uses)
        image_rgb = image[:, :, ::-1]

    except:
        raise HTTPException(
            status_code=422, detail="Unable to process file"
        )
    # Find all the faces and face encodings in the current frame of video
    time_start = time.time()
    face_locations = face_recognition.face_locations(image_rgb)
    print(f"time for face locations: {time.time() - time_start}")

    time_start = time.time()
    face_encodings = face_recognition.face_encodings(image_rgb, face_locations, model="small")
    print(f"time for face envodings: {time.time() - time_start}")

    time_start = time.time()
    face_landmarks_list = face_recognition.face_landmarks(image_rgb, face_locations)
    print(f"time for face landmarks: {time.time() - time_start}")

    # filter for lip related landmarks
    important_landmarks = []
    for e in face_landmarks_list:
        for k, v in e.items():
            important_landmarks.append(list(v))

    return {"face_locations":[list(f) for f in face_locations], "face_encodings":[list(f) for f in face_encodings], "face_landmarks":[dict(f) for f in face_landmarks_list]}

if __name__ == '__main__':
    uvicorn.run(app,
            host='127.0.0.1',
            port=8000
           )