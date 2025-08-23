

int value;
int tmp_sensor = A0;
float voltage;
float temperatureC;

void setup() {
  Serial.begin(9600);
  pinMode(tmp_sensor, INPUT);
}

void loop() {
  value = analogRead(tmp_sensor);               // 아날로그 값 읽기
  voltage = value * 5.0 / 1023.0;               // 전압 변환
  temperatureC = voltage / 0.01;                // 온도로 변환 (1V = 100°C 가정)

  Serial.print("Temperature: ");
  Serial.print(temperatureC);
  Serial.println(" C");

  // 조건 체크
  if (temperatureC >= 30) {
    Serial.println("⚠️ Warning: Temperature is above 30°C!");
  }

  if (temperatureC <= 10) {
    Serial.println("⚠️ Warning: Temperature is below 10°C!");
  }

  delay(200);  // 0.2초 간격으로 측정
}
