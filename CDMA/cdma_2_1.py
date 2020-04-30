#!/usr/bin/python
import serial
import RPi.GPIO as GPIO
import time
import multiprocessing

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(17, GPIO.IN)
GPIO.setup(24, GPIO.OUT)
GPIO.setwarnings(False)

def receiver():
        ser= serial.Serial(port='/dev/ttyACM0', baudrate=115200)
        while True:
                # Receives analog readings from Arduino at 100 Hz
                line = ser.readline()
                line = line.rstrip()
                print line
        ser.close()


def sender1():
		 #Setting i/p to 00,01,10,11 for 5 secs
         while 1:
                print("00")
                GPIO.output(23, GPIO.LOW)
                GPIO.output(24, GPIO.LOW)
                time.sleep(5)

                print("01")
                GPIO.output(23, GPIO.LOW)
                GPIO.output(24, GPIO.HIGH)
                time.sleep(5)

                print("10")
                GPIO.output(23, GPIO.HIGH)
				GPIO.output(24, GPIO.LOW)
                time.sleep(5)

                print("11")
                GPIO.output(23, GPIO.HIGH)
                GPIO.output(24, GPIO.HIGH)
                time.sleep(5)


if __name__ == "__main__":
        p1 = multiprocessing.Process(target = sender1)
        p3 = multiprocessing.Process(target = receiver)
        p3.start()
        p1.start()
