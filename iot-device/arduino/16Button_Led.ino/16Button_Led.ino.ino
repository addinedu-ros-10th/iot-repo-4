#include <Keypad.h> // 키패드 라이브러리

const byte ROWS = 4; // 4개의 가로줄
const byte COLS = 4; // 4개의 세로줄
char hexaKeys[ROWS][COLS] = { // 키패드 버튼 위치
  {'1','2','3','4'},
  {'5','6','7','8'},
  {'9','A','B','C'},
  {'*','0','#','D'}
};

byte rowPins[ROWS] = {9, 8, 7, 6}; // 키패드 가로 연결핀 번호
byte colPins[COLS] = {5, 4, 3, 2}; // 키패드 세로 연결핀 번호

Keypad key = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

// LED 핀 번호 (총 8개: 10~13, A0~A3)
const int ledPins[8] = {13, 12, 11, 10, A0, A1, A2, A3};
// LED 상태 저장 배열
bool ledStates[8] = {false, false, false, false, false, false, false, false};

void setup() {
  Serial.begin(9600); // 시리얼 통신 시작
  for (int i = 0; i < 8; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW); // 처음엔 꺼진 상태
  }
}

void loop() {
  char myKey = key.getKey(); // 키패드 입력값 저장
  if (myKey) {
    Serial.println(myKey); // 입력값 출력

    // '1'~'8' 버튼 → LED 제어
    if (myKey >= '1' && myKey <= '8') {
      int index = myKey - '1';   // '1'→0, '2'→1, ... '8'→7
      ledStates[index] = !ledStates[index]; // 상태 토글
      digitalWrite(ledPins[index], ledStates[index] ? HIGH : LOW);
    }
  }
}
