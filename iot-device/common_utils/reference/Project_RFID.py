import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
from PyQt6.QtCore import *
import time

import serial



from_class = uic.loadUiType("Project_RFID.ui")[0]

class Receiver(QThread):
    sig_bytes = pyqtSignal(str)
    recvTotal = pyqtSignal(int)
    sig = pyqtSignal()

    def __init__(self, conn, parent=None):
        super(Receiver, self).__init__(parent)
        self.is_running = False
        self.conn = conn
        print("recv init")

    def run(self):
        self.is_running = True
        led_status = False
        while (self.is_running == True):
            if self.conn.readable():
                res = self.conn.readline().decode().strip('\r\n')

                if res.startswith("read"):
                    self.sig_bytes.emit(res)
                    self.conn.write(b'H')
                    led_status = True
                # else :
                #     print("else")
                #     print(led_status)
                #     if led_status:
                #         self.conn.write(b'L')
                #         led_status = False

    def stop(self):
        print("recv stop")
        self.is_running = False

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.uid = bytes(4)
        self.conn = serial.Serial(port = '/dev/ttyACM0', baudrate=9600, timeout=1)
        self.recv = Receiver(self.conn)
        self.recv.start()
        self.recv.sig_bytes.connect(self.print)

        self.pushButton.clicked.connect(self.high)
        self.pushButton_2.clicked.connect(self.low)        


    def high(self):
        print("HIGH")
        self.conn.write(b'H')
        return
    
    def low(self):
        print("LOW")
        self.conn.write(b'L')
        return
    
    def print(self, cmd):
        print(str(cmd))
        self.lineEdit.setText(cmd)
        
        return

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec())