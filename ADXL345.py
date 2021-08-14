from machine import Pin,I2C
import math
import time

device = 0x18
regAddress = 0x28
TO_READ = 6
buff = bytearray(6)

class ADXL345:
    def __init__(self,i2c,addr=device):
        self.addr = addr
        self.i2c = i2c
        self.i2c.writeto_mem(self.addr,0x25,0x64)#enabled sensor ic by writing to control register 

        self.i2c.writeto_mem(self.addr,0x04,0x25)#enabled sensor ic by writing to control register 
    
    def xValue(self):
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ) #read 6 bytes of data from register address
        x = (int(buff[1]) << 8) | buff[0] #Parse data
        if x > 32767:
            x -= 65536
        return x
   
    
    def yValue(self):
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ) #read 6 bytes of data from register address
        y = (int(buff[3]) << 8) | buff[2]#Parse data
        if y > 32767:
            y -= 65536
        return y
     
       
    def zValue(self): 
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)#read 6 bytes of data from register address
        z = (int(buff[5]) << 8) | buff[4]#Parse data
        if z > 32767:
            z -= 65536
        return z
           
    def RP_calculate(self,x,y,z):   #formula from datasheet
        roll = math.atan2(y , z) * 57.3
        pitch = math.atan2((- x) , math.sqrt(y * y + z * z)) * 57.3
        return roll,pitch
    
    
i2c = I2C("I2C_0") #Initialise I2C instance
adx = ADXL345(i2c)
while True:
    x=adx.xValue()
    y=adx.yValue()
    z=adx.zValue()
    print(x,y,z)
