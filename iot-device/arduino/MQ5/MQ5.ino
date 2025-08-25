int GasPin = A0;
float RL = 10.0;   // kΩ

// 센서별 보정값 및 근사식
float R0;
float m, b;

void setup() {
  Serial.begin(57600);

    R0 = 6.5;   // 공기 중 Rs/R0
    m = -0.45;  
    b = 1.52;   

}

void loop() {
  int adcValue = analogRead(GasPin);
  float Vout = adcValue * (5.0 / 1023.0);
  float Rs = (5.0 - Vout) * RL / Vout;
  float ratio = Rs / R0;

  float ppm = pow(10, (log10(ratio) - b) / m);

  byte buffer[8];
  union data_u{
    float i;
    unsigned char bytes[sizeof(float)];
  };

  data_u data;

  data.i = ppm;

  memset(buffer, 0x00, sizeof(buffer));
  memset(buffer, 0x04, 1);
  memset(buffer+1, 0x01, 1);
  memset(buffer+2, 0xFD, 1);
  memcpy(buffer+3, data.bytes, sizeof(float));
  memset(buffer+7, 0xFA, 1);
  Serial.write(buffer, sizeof(buffer));
  Serial.println();

  delay(300);
}
