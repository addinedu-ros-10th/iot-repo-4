int GasPin = A0;
float RL = 10.0;   // kΩ

// 센서 선택 (5 → MQ-5, 7 → MQ-7)
int sensorType = 7;

// 센서별 보정값 및 근사식
float R0;
float m, b;

void setup() {
  Serial.begin(9600);

  if (sensorType == 5) {
    // MQ-5 (LPG)
    R0 = 6.5;   // 공기 중 Rs/R0
    m = -0.45;  
    b = 1.52;   
  } else if (sensorType == 7) {
    // MQ-7 (CO)
    R0 = 10.0;  // 공기 중 Rs/R0
    m = -0.77;
    b = 1.7;
  }
}

void loop() {
  int adcValue = analogRead(GasPin);
  float Vout = adcValue * (5.0 / 1023.0);
  float Rs = (5.0 - Vout) * RL / Vout;
  float ratio = Rs / R0;

  float ppm = pow(10, (log10(ratio) - b) / m);


  if (sensorType == 5) Serial.print("MQ-5 ppm: ");

      byte buffer[8];
      union data_u{
        float i;
        unsigned char bytes[sizeof(float)];
      };

      data_u data;

      data.i = LoadCell.getData() * 0.03011;

      memset(buffer, 0x00, sizeof(buffer));
      memset(buffer, 0x04, 1);
      memset(buffer+1, 0x00, 1);
      memset(buffer+2, 0xFD, 1);
      memcpy(buffer+3, data.bytes, sizeof(float));
      memset(buffer+7, 0xFA, 1);
      Serial.write(buffer, sizeof(buffer));
      Serial.println();
      
  if (sensorType == 7) Serial.print("MQ-7 ppm: ");
  Serial.println(ppm);

  delay(300);
}
