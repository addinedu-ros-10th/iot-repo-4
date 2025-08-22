
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
from PyQt6.QtCore import *
import time
import serial
from rest_transport import RestTransport

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

                if len(res) > 0:
                    self.sig_bytes.emit(res)
                    # self.conn.write(b'H')
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


class PostThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, payload):
        super().__init__()
        self.payload = payload

    def run(self):
        rt = RestTransport()
        res = rt.post_json("/api/users/create", self.payload)
        self.finished.emit(res)

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.uid = bytes(4)
        self.conn = serial.Serial(port = '/dev/ttyACM0', baudrate=9600, timeout=1)
        self.recv = Receiver(self.conn)
        self.recv.start()
        self.recv.sig_bytes.connect(self.print)
        self.server = 7

        self.pushButton.clicked.connect(self.high)
        self.pushButton_2.clicked.connect(self.low)

    def high(self):
        print("HIGH")
        self.conn.write(b'H')
        self.server += 1
        self.test_post_json()
        return

    def low(self):
        print("LOW")
        self.conn.write(b'L')
        self.server += 1
        self.test_post_json()
        return

    def print(self, cmd):
        print(str(cmd))
        self.lineEdit.setText(cmd)
        return

    def get_server(self):
        return self.server

    def test_post_json(self):
        # 중복되지 않는 값 생성 (user_name/email에 시간+랜덤값 사용)
        import uuid, datetime
        unique_id = uuid.uuid4().hex[:8]
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        user_name = f"create_{now}_{unique_id}"
        email = f"{user_name}@example.com"
        phone_number = "01023222545"  # 유효성 검증 통과하는 값
        user_role = "admin"
        payload = {
            "user_name": user_name,
            "email": email,
            "phone_number": phone_number,
            "user_role": user_role
        }
        self.post_thread = PostThread(payload)
        self.post_thread.finished.connect(self.handle_post_response)
        self.post_thread.start()

    def handle_post_response(self, res):
        # 결과를 콘솔과 UI에 모두 출력
        try:
            if hasattr(res, 'text'):
                self.lineEdit.setText(res.text)
                print(f"Response: {res.text}")
            else:
                self.lineEdit.setText(str(res))
                print(f"Response: {res}")
        except Exception as e:
            self.lineEdit.setText(f"Error: {e}")
            print(f"Error: {e}")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec())