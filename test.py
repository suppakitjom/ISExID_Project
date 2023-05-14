import pynput
from pynput.keyboard import Key, Controller
import random

keyboard = Controller()
import time
while True:
    #randomly press 1,2,3,4
    x = str(random.randint(1, 4))
    keyboard.press(x)
    keyboard.release(x)
    time.sleep(2)
