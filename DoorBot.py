import RPi.GPIO as gpio
import time
from time import sleep
from firebase import firebase
gpio.setwarnings(False)

sensor = 27
buzzerPin = 17
ledPin = 24

gpio.setmode(gpio.BCM)
gpio.setup(sensor,gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(buzzerPin, gpio.OUT)
gpio.setup(ledPin, gpio.OUT)

firebase = firebase.FirebaseApplication('https://smart-b748c-default-rtdb.firebaseio.com/', None)


previous = "null"

while True:
    state = gpio.input(sensor)
    if state == False and previous == "open" or state == False and previous == "null":
        print('Door closed')
        gpio.output(buzzerPin, 0)
        gpio.output(ledPin, 0)
        firebase.put('/', 'doorStatus', 'true')
        previous = "closed"
    if state != False and previous == "closed" or state != False and previous == "null":
        print('Door open')
        results = firebase.get('alarmStatus', None)
        if(results==True):
            gpio.output(buzzerPin, 1)
            gpio.output(ledPin, 1)
        firebase.put('/', 'doorStatus', 'false')
        previous = "open"
    sleep(0.1)
    
gpio.cleanup(sensor)