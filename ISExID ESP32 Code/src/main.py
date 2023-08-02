import serial
from pynput.keyboard import Key, Controller

keyboard = Controller()

PORT = '/dev/cu.usbmodem2101'

ser = serial.Serial(PORT, 9600)

while True:
    text = ser.readline().strip().decode('utf-8')
    print(text)
    # simulate keyboard press
    if text == '1':
        keyboard.press('1')
        keyboard.release('1')
    elif text == '2':
        keyboard.press('2')
        keyboard.release('2')
    elif text == '3':
        keyboard.press('3')
        keyboard.release('3')
    elif text == '4':
        keyboard.press('4')
        keyboard.release('4')
    elif text == '5':
        keyboard.press('5')
        keyboard.release('5')
    elif text == '6':
        keyboard.press('6')
        keyboard.release('6')
