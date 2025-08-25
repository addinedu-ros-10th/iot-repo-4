// 팅커캐드 주소 -> https://www.tinkercad.com/things/4QOHrIpD3BI/editel?returnTo=%2Fdashboard%2Fcollections%2Fcjqy9BHSKvc%2Fcircuits
// 두세트만 예시로 올려놓고 나머지는 동일한 로직으로 나머지 4개 옆으로 쫘라락 배치하면됨 

// 6개의 버튼(입력)과 LED(출력) 쌍을 제어
const uint8_t outputPins[6] = {13, 11, 9, 7, 5, 3};
const uint8_t inputPins[6]  = {12, 10, 8, 6, 4, 2};

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 6; i++) {
    pinMode(outputPins[i], OUTPUT);
    pinMode(inputPins[i], INPUT);   
  }
}

void loop() {
  int val = 0;
  // for (int i = 0; i < 6; i++) {
  // val = digitalRead(inputPins[i]);
  val = digitalRead(12);

  //   if (val == HIGH) {  
  //     // 버튼 눌렸을 때만 출력
  //     Serial.print("Button ");
  //     Serial.print(i + 1);
  //     Serial.println(" pressed");

  //     digitalWrite(outputPins[i], HIGH);
  //   } 
  //   else {
  //     digitalWrite(outputPins[i], LOW);
  //   }
  // }


  unsigned long now = millis() / 1000;

  Serial.print("{");
  Serial.print("sensor-type : " );
  Serial.print("MQ-5");
  Serial.print(", ");
  Serial.print("sensing-unit : " );
  Serial.print("on/off");
  Serial.print(", ");
  Serial.print("sensor-location : " );
  Serial.print("ketchen");
  Serial.print(", ");
  Serial.print("data-type : " );
  Serial.print("boolean");
  Serial.print(", ");
  Serial.print("value : " );
  Serial.print(val);
  Serial.print(", ");
  Serial.print("timestamp : " );
  Serial.print(now);
  Serial.print("}");
  Serial.println();

  delay(50); // 빠른 중복 출력 방지
}
