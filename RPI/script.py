import serial
import RPi.GPIO as GPIO
from machine import I2C
from python_lcd.lcd import LcdApi
from i2c_lcd import I2cLcd  

led2 = 2 
led3 = 3
led4 = 4  
led5 = 5
led6 = 6
led7 = 7
led8 = 8
led9 = 9

GPIO.setmode(GPIO.BCM)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)
GPIO.setup(led5, GPIO.OUT)
GPIO.setup(led6, GPIO.OUT)
GPIO.setup(led7, GPIO.OUT)
GPIO.setup(led8, GPIO.OUT)
GPIO.setup(led9, GPIO.OUT)

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)  

try:
    while True:
        if ser.in_waiting > 0:  
            data = ser.read(ser.in_waiting).decode('utf-8').strip()  
            if d1 == 1:
                GPIO.output(led2, GPIO.HIGH)
                GPIO.output(led3, GPIO.LOW)  
                
            elif:
                GPIO.output(led3, GPIO.HIGH)  
                GPIO.output(led2, GPIO.LOW)

            if d2 == 1:
                GPIO.output(led4, GPIO.HIGH)
                GPIO.output(led5, GPIO.LOW)  
                
            elif:
                GPIO.output(led5, GPIO.HIGH)  
                GPIO.output(led4, GPIO.LOW)

            if d3 == 1:
                GPIO.output(led6, GPIO.HIGH)
                GPIO.output(led7, GPIO.LOW)  
                
            elif:
                GPIO.output(led7, GPIO.HIGH)  
                GPIO.output(led6, GPIO.LOW)

            if d4 == 1:
                GPIO.output(led8, GPIO.HIGH)
                GPIO.output(led9, GPIO.LOW)  
                
            elif:
                GPIO.output(led9, GPIO.HIGH)  
                GPIO.output(led8, GPIO.LOW)
                
except KeyboardInterrupt:
    print("Programme arrêté")
finally:
    GPIO.cleanup()  
    ser.close()     

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)  
I2C_ADDR = 0x27
ROWS = 2
COLS = 16
lcd = I2cLcd(i2c, I2C_ADDR, ROWS, COLS)
lcd.clear()
lcd.putstr("Park smartly")  
lcd.move_to(0, 1)           
lcd.putstr("with AI") 