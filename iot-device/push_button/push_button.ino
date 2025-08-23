bool ledBlinking = false;   // LED 깜빡임 상태 저장
int prevButton = LOW;       // 이전 버튼 상태 저장

void setup(){
  pinMode(11, OUTPUT);   // LED
  pinMode(7, INPUT);     // 스위치 버튼
  Serial.begin(9600);
}

void loop(){
  int button = digitalRead(7);

  // 버튼이 눌릴 때만 토글 (HIGH로 변할 때)
  if(button == HIGH && prevButton == LOW){
    ledBlinking = !ledBlinking;  // 상태 반전
    if(ledBlinking){
      Serial.println("관리자 호출 시작");
    } else {
      Serial.println("관리자 호출 종료");
      digitalWrite(11, LOW);     // LED 끄기
    }
    delay(200); // 버튼 바운스 방지 (0.2초)
  }
  prevButton = button;

  // LED 깜빡이기
  if(ledBlinking){
    digitalWrite(11, HIGH);
    delay(300);               // 0.3초 ON
    digitalWrite(11, LOW);
    delay(300);               // 0.3초 OFF
  }
}
