int GasPin = A0;
float RL = 10.0;   // kΩ
const int LED_PIN = 7;

// 센서 선택 (5 → MQ-5, 7 → MQ-7)
int sensorType = 7;

// 센서별 보정값 및 근사식
float R0;
float m, b;

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);

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
	
  
  // LED Control
  int recv_size = 0;
	char recv_buffer[16];  
  if (Serial.available() > 0)
  {
    recv_size = Serial.readBytesUntil('\n', recv_buffer, 16);
  }
  if (recv_size > 0)
  {
    char cmd[2];
    memset(cmd, 0x00, sizeof(cmd));
    memcpy(cmd, recv_buffer, 1);

    if (strncmp(cmd, "H", 1) == 0)
		{
			digitalWrite(LED_PIN, HIGH);
		}
		else if (strncmp(cmd, "L", 1) == 0)
		{
			digitalWrite(LED_PIN, LOW);
		}
	}

  int adcValue = analogRead(GasPin);
  float Vout = adcValue * (5.0 / 1023.0);
  float Rs = (5.0 - Vout) * RL / Vout;
  float ratio = Rs / R0;

  float ppm = pow(10, (log10(ratio) - b) / m);


  if (sensorType == 5) Serial.print("MQ-5 ppm: ");
  if (sensorType == 7) Serial.print("MQ-7 ppm: ");
  Serial.println(ppm);





  delay(300);
}
