import serial
import datetime
import csv
import struct
data_list = ""
conn = serial.Serial(port= "/dev/ttyACM0", baudrate = 57600, timeout=1)
# file = open('test.log', 'w', newline='')
while(True):
    if (conn.readable()):
        data = conn.read_until(b'\r\n')
        print(data[3:7])

        try:
            data_list = str(struct.unpack("f",data[3:7])) + " " + str(datetime.datetime.now()) + "\n"
        except:
            data_list = 0
        print(data_list)
        # file.write(data_list)
        # file.flush()
    else:
        pass
        # conn.close()
        # file.close()
    

