import logging
import os
from datetime import datetime
import cv2
from tensorflow.keras.applications.vgg16 import preprocess_input
import tensorflow as tf
import numpy as np

def write_text_cam(text, frame, col, offset, x, y):

    cv2.putText(
    frame,
    text,
    (x-offset-10,y-offset-10), 
    cv2.FONT_HERSHEY_SIMPLEX, 
    1, 
    col,
    2,
    cv2.LINE_AA
    )

def write_image(out, frame):
    """
    writes frame from the webcam as png file to disk. datetime is used as filename.
    """
    if not os.path.exists(out):
        os.makedirs(out)
    now = datetime.now() 
    dt_string = now.strftime("%H-%M-%S-%f") 
    filename = f'{out}/{dt_string}.png'
    logging.info(f'write image {filename}')
    cv2.imwrite(filename, frame)


def key_action():
    # https://www.ascii-code.com/
    k = cv2.waitKey(1)
    if k == 113: # q button
        return 'q'
    if k == 32: # space bar
        return 'space'
    if k == 112: # p key
        return 'p'
    return None


def init_cam(width, height):
    """
    setups and creates a connection to the webcam
    """

    logging.info('start web cam')
    cap = cv2.VideoCapture(0)

    # Check success
    if not cap.isOpened():
        raise ConnectionError("Could not open video device")
    
    # Set properties. Each returns === True on success (i.e. correct resolution)
    assert cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    assert cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    return cap



def get_predicted_label(model, image, classes):

    # img = preprocess_input(image)
    image = np.expand_dims(image, axis = 0)
    class_idx = np.argmax(model.predict(image), axis = 1)

    return classes[class_idx[0]]

