#!/usr/bin/python
import serial
import RPi.GPIO as GPIO
import time
import multiprocessing

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

#Dot product of chipping sequence and received bits
def multiply(a,b):
                res=0
                for i in range(0,4):
                        res = res+a[i]*b[i]
                return res


def receiver():
                global tmp
                while(time.time()<tmp+0.1):
                        pass
                ser= serial.Serial(port='/dev/ttyACM0', baudrate=115200)
                ser.flushInput()
                tx1_1=[1,1,1,1] #chipping sequence for transmitter 1
                tx2_1=[1,1,-1,-1] #chipping sequence for transmitter 2
                p=0
                for p in range(0,18):
                        out1='' #Received chips from 1
                        out2='' #received chips from 2
                        for m in range(0,7):
                                res =[]
                                i=0
                                while i<4:
                                        line = ser.readline()
                                        line = line.rstrip()
                                        q=int(line,10)
                                        if(q>900): #transmitted bits are 11
                                                res.insert(i,2)
                                        elif(q>300): #transmitted bits are 01 or 10
                                                res.insert(i,0)
                                        else: #transmitted bits 00
                                                res.insert(i,-2)
                                        i=i+1

                                res_tx1 = multiply(tx1_1,res)
                                res_tx2 = multiply(tx2_1,res)
                                #dot product >0, initial bit to be transmitted was 1 from sender
                                if(res_tx1>0):
                                                out1=out1+'1'
                                else:
                                                out1=out1+'0'

                                if(res_tx2>0):
                                                out2=out2+'1'
                                else:
                                                out2=out2+'0'
                        #group the 7 initial bits and convert to ascii and then to chr
                        if out1!='':
                                print(chr(int(out1,2))),
                        if out2!='':
                                print(chr(int(out2,2))),
                ser.close()

def sender1():
         #tmp used for synchronisation of processes
         global tmp
         while(time.time()<tmp+0.1):
                pass
         s = 'HELLO FROM SENDER1'
         for h in range(0,18): #length of s =18
                i = 0
                while i<len(s):
                        m = format(ord(s[i]), '07b')#convert chr to ascii and then to bits
                        j=0
                        while j<len(m):
                                #multiply the bit with chipping sequence
                                if m[j] == '0':
                                         v =0
                                         for v in range(0,4):# 4 bit chipping sequence
                                                if v==0 :
                                                        GPIO.output(23, GPIO.HIGH)
                                                if v==1 :
                                                        GPIO.output(23, GPIO.HIGH)
                                                if v==2 :
                                                        GPIO.output(23, GPIO.HIGH)
                                                if v==3 :
                                                        GPIO.output(23, GPIO.HIGH)

                                                t= time.time()
                                                while(time.time()<(t+.01)):
                                                        pass
                                if m[j] == '1':
                                         x=0
                                         for x in range(0,4):
                                                if x==0 :
                                                        GPIO.output(23, GPIO.LOW)
                                                if x==1 :
                                                        GPIO.output(23, GPIO.LOW)
                                                if x==2 :
                                                        GPIO.output(23, GPIO.LOW)
                                                if x==3 :
                                                        GPIO.output(23, GPIO.LOW)
                                                #0.01s is used as sampling freq is 100Hz
                                                t= time.time()
                                                while(time.time()<(t+.01)):
                                                        pass
                                j=j+1
                        i=i+1

def sender2():
		 #tmp used for synchronisation of processes
         global tmp
         while(time.time()<tmp+0.1):
                pass
         s = 'hello from sender2'
         for h in range(0,18):#length of s =18
                i = 0
                while i<len(s):
                        m = format(ord(s[i]), '07b')#convert chr to ascii and then to bits
                        j=0
                        while j<len(m):
								#multiply the bit with chipping sequence
                                if m[j] == '0':
                                         v =0
                                         for v in range(0,4):# 4 bit chipping sequence
                                                if v==0 :
                                                        GPIO.output(24, GPIO.HIGH)
                                                if v==1 :
                                                        GPIO.output(24, GPIO.HIGH)
                                                if v==2 :
                                                        GPIO.output(24, GPIO.LOW)
                                                if v==3 :
                                                        GPIO.output(24, GPIO.LOW)

                                                t= time.time()
                                                while(time.time()<(t+.01)):
                                                        pass
                                if m[j] == '1':
                                         x=0
                                         for x in range(0,4):
                                                if x==0 :
                                                        GPIO.output(24, GPIO.LOW)
                                                if x==1 :
                                                        GPIO.output(24, GPIO.LOW)
                                                if x==2 :
                                                        GPIO.output(24, GPIO.HIGH)
                                                if x==3 :
                                                        GPIO.output(24, GPIO.HIGH)
												#0.01s is used as sampling freq is 100Hz
                                                t= time.time()
                                                while(time.time()<(t+.01)):
                                                        pass
                                j=j+1
                        i=i+1

if __name__ == "__main__":
        global tmp
        while True:
                tmp = time.time()
                p3 = multiprocessing.Process(target = sender1)
                p2 = multiprocessing.Process(target = sender2)
                p1 = multiprocessing.Process(target = receiver)
                GPIO.output(23, GPIO.LOW)
                GPIO.output(24, GPIO.LOW)
                p1.daemon = True # To avoid subprocesses hampering main process
                p2.daemon = True
                p3.daemon = True
                p1.start()
                p2.start()
                p3.start()
                time.sleep(6)
                p1.terminate() # Terminates process
                p2.terminate()
                p3.terminate()
                p1.join()
                p2.join()
                p3.join()
