import numpy as np
import cv2
import base64

def preprocess_image(image):
    image = base64.b64decode(image)
    image = np.frombuffer(image, dtype=np.uint8)
    image = cv2.imdecode(image, flags=1)
    image = np.array([image])
    return image