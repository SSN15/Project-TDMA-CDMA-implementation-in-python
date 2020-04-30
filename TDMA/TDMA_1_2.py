#!/usr/bin/python
from __future__ import print_function
import RPi.GPIO as GPIO
import time
import multiprocessing

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(17, GPIO.IN)
GPIO.setup(24, GPIO.OUT)

def sender1():
         s = 'HELLO FROM SENDER1'
         while 1:
				#Synchronisation - all processes to start at the same time
                t=time.time()
                while(time.time()<(t+0.002)):
                        pass
                i = 0
                while i<len(s): 
                        m = format(ord(s[i]), '07b')#convert chr to ascii and then to bits
                        j=0
                        while j<len(m): #length of ascii to be transmitted
                                if m[j] == '0':
                                        GPIO.output(23, GPIO.HIGH)
										#time for 1 bit to be transmitted (bit rate = 1/0.0125 = 80bits/sec)
                                        t= time.time()
                                        while(time.time()<(t+0.0125)):
                                                pass
                                else:
                                        GPIO.output(23, GPIO.LOW)
                                        t= time.time()
                                        while(time.time()<(t+0.0125)):
                                                pass
                                j=j+1
                        i=i+1
                        GPIO.output(23, GPIO.LOW)
						#waiting time for one character to be sent from the other sender
                        t= time.time()
                        while(time.time()<(t+0.0875)):
                                pass

def sender2():
         s = 'hello from sender2'
         while 1:
                t=time.time()
                while(time.time()<(t+0.002)):
                        pass
                i = 0
                while i<len(s):
						#waiting time for one character to be sent from the other sender
                        GPIO.output(24, GPIO.LOW)
                        t=time.time()
                        while(time.time()<(t+0.0875)):
                                pass
                        m =format(ord(s[i]), '07b')#convert chr to ascii and then to bits
                        j=0
                        while j<len(m): #length of ascii to be transmitted
                                if m[j] == '0':
                                        GPIO.output(24, GPIO.HIGH)
										#time for 1 bit to be transmitted (bit rate = 1/0.0125 = 80bits/sec)
                                        t= time.time()
                                        while(time.time()<(t+0.0125)):
                                                pass
                                else:
                                        GPIO.output(24, GPIO.LOW)
                                        t= time.time()
                                        while(time.time()<(t+0.0125)):
                                                pass
                                j=j+1
                        i=i+1
def receiver():			
						#for synchronisation
                        t= time.time()
                        while(time.time()<(t+0.00825)):
                                pass
                        res=""
                        while 1:
                                z=""
                                for v in range(0,7):
                                        c = (GPIO.input(17))
                                        z=z+str(c)
										#time for 1 bit to be transmitted (bit rate = 1/0.0125 = 80bits/sec)
                                        t= time.time()
                                        while(time.time()<(t+0.0125)):
                                               pass
                                res=res+chr(int(z,2)) #group the 7 bits and convert to ascii and then to chr
                                print(res),
                                

if __name__ == "__main__":

        p1 = multiprocessing.Process(target = sender1)
        p2 = multiprocessing.Process(target = sender2)
        p3 = multiprocessing.Process(target = receiver)
        time.sleep(3)
        p3.start()
        p2.start()
        p1.start()
								