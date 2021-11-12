# Arda Mavi
import torch
import os
import sys
import platform
import numpy as np
from time import sleep
import time
from PIL import Image
from game_control import *
from predict import predict
from scipy.misc import imresize
from game_control import get_id
from get_dataset import save_img
from multiprocessing import Process
from keras.models import model_from_json
from pynput.mouse import Listener as mouse_listener
from pynput.keyboard import Listener as key_listener
import string
from threading import *
import keyboard as kb
from mss import mss
def get_screenshot():
    with mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        img = np.array(img)[:,:,:3] # Get first 3 channel from image as numpy array.
        img = imresize(img, (150, 150, 3)).astype('float32')/255.
        return img

def save_event_keyboard(data_path, event, key):
    key = get_id(key)
    if key == 1000:
        return
    else:
        data_path = data_path + '/-1,-1,{0},{1},{2}'.format(event, key, time.time())
        screenshot = get_screenshot()
        save_img(data_path, screenshot)
        return

def save_event_mouse(data_path, x, y):
    data_path = data_path + '/{0},{1},0,0,{2}'.format(x, y, time.time())
    screenshot = get_screenshot()
    save_img(data_path, screenshot)
    return

def listen_mouse():
    data_path = 'Data/Train_Data/Mouse'
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    def on_click(x, y, button, pressed):
        save_event_mouse(data_path, x, y)

    def on_scroll(x, y, dx, dy):
        pass

    def on_move(x, y):
        pass

    with mouse_listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()

def listen_keyboard():
    data_path = 'Data/Train_Data/Keyboard'
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    def on_press(key):
        save_event_keyboard(data_path, 1, key)

    def on_release(key):
        save_event_keyboard(data_path, 2, key)

    with key_listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    dataset_path = 'Data/Train_Data/'
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    # Start to listening mouse with new process:
    Process(target=listen_mouse, args=()).start()
    listen_keyboard()

    return

if __name__ == '__main__':
    main()
