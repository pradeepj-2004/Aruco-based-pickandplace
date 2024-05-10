
import math
from math import sin, cos, atan, pi, atan2, sqrt, acos

import serial
import time
# lenghts of links
l1= 12
l2= 12

serial_port = '/dev/ttyACM0'  # Change this to match your serial port
baud_rate = 9600

# Initialize the serial connection
# ser = serial.Serial(serial_port, baud_rate, timeout=1)

def base_angle(x,y):

    theta_0= math.atan(y/x)*180/3.14
    print("base_angle:",theta_0)
    return theta_0

def angles(l1,l2,x,y):

    A=y
    B=x

    C=(l1**2 - l2**2 + x**2 + y**2)/(2*l1) 
    th1_1= 2*atan2(A-sqrt(A*A + B*B -C*C),(B+C))
    th1_2=atan2((y-l1*sin(th1_1)),x-l1*cos(th1_1))  -th1_1      

  
    print("th1_1: ",th1_1*180/pi)
    print("th1_2: ",th1_2*180/pi)

    th2_1= 2*atan2(A+sqrt(A*A + B*B -C*C),(B+C))
    th2_2=atan2((y-l1*sin(th2_1)),x-l1*cos(th2_1))  -th2_1  

    print("th2_1: ",th2_1*180/pi)
    print("th2_2: ",th2_2*180/pi)

    return th2_1*180/pi,th2_2*180/pi

def main():
    x= float(input("enter x coordinate:"))
    y= float(input("enter y coordinate:"))
    if y>0:
        y=y+1.0
    elif y<0:
        y=y+1.0
        x=x+1.5
    theta_base=base_angle(x,y)

    theta_2,theta_3=angles (12,12,sqrt(x**2+(y)**2)-8,-3)
    
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    i=0
    try:
        while True:
            if i==0:
                values = [int(theta_base),int(theta_2),abs(int(theta_3)),25,int(abs(theta_3)-theta_2),0]
            if i==1:
                values = [int(theta_base),int(theta_2),abs(int(theta_3)),25,int(abs(theta_3)-theta_2),67]
            if i==2:
                values=[0,170,0,35,0,60]
            
            if i==3:
                values=[0,170,0,35,0,40]
            
            if i==4:
                values=[20,135,130,35,90,0]
                
            # Convert the list to a string with comma-separated values
            data_to_send = ' '.join(map(str, values))
            ser.write(data_to_send.encode('utf-8'))
            received = ser.readline().decode('utf-8').strip()
            print(data_to_send,received)
            if (received==data_to_send):
                i=i+1
                time.sleep(2)
                if i==5:
                    break       

            time.sleep(4)

    except KeyboardInterrupt:
        # Close the serial connection when Ctrl+C is pressed
        ser.close()
    

if __name__ =='__main__':
    main()



