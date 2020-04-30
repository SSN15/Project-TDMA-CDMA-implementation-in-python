#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import multiprocessing

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT) 									#Output pin 23
GPIO.setup(17, GPIO.IN)	 									#Input pin 17

def sender():
         while 1:
                i = 0
                s = 'Hello World!!' 
                while i<len(s): 							#Running for the entire length of the string
                        m = bin(ord(s[i])) 					#Converting ASCII to Binary
                        n=m[2:] 							#Truncating 0 and b 
                        j=0
                        length = 7 - len(n) 				#python truncates all trailing zeroes; length calculates the number of trailing zeroes
                        if(len(n)<7):						#to add the trailing zeroes so as to make all the characters of length 7 in binary
                                for k in range(0,length):
                                        n='0'+n
                        while j<len(n):						#Active LOW ; converting all binary inputs to LED outputs
                                if n[j] == '0':
                                        GPIO.output(23, GPIO.HIGH)
                                        time.sleep(.1)
                                else:
                                        GPIO.output(23, GPIO.LOW)
                                        time.sleep(.1)
                                j=j+1
                        i=i+1


def receiver():
                        res=""								#Received string
						while 1:
                                z=""						#Storing the binary sequence for the individual characters
                                for v in range(0,7):
                                        c = (GPIO.input(17))
                                        z=z+str(c)			#Concatenating the last received bit with previous bits
                                        time.sleep(.1) 		#to synchronize with input
                                res=res+chr(int(z,2)) 		#to store the entire string; converting from base2 to base10; DECODING
                                print(res)

if __name__ == "__main__":
        p1 = multiprocessing.Process(target = sender) 		#Sender Process 
        p2 = multiprocessing.Process(target = receiver)		#Receiver Process 
        p1.start()											#Start sender
		p2.start()											#Start reciver