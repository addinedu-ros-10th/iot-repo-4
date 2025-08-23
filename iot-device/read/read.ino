int reedPin = 2;    // 리드 스위치 입력 핀
int ledPin = 8;    // LED 출력 핀
int reedState = 0;  // 리드 스위치 상태 저장 변수

void setup() {
  pinMode(reedPin, INPUT);    // 입력 설정
  pinMode(ledPin, OUTPUT);    // 출력 설정
  Serial.begin(9600);         // 시리얼 통신 시작
}

void loop() {
  reedState = digitalRead(reedPin);  // 리드 스위치 상태 읽기

  if (reedState == HIGH) {
    digitalWrite(ledPin, HIGH);      // 자석이 감지되면 LED 켜기
    Serial.println("자석 감지됨!");
  } else {
    digitalWrite(ledPin, LOW);       // 감지되지 않으면 LED 끄기
    Serial.println("자석 없음");
  }

  delay(300);
}
