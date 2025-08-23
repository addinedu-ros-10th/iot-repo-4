int analogPin = A0;
int ledPin = 13;
int analogVal = 0;
long int past_time = 0;
int past_analogVal = 0;

void setup() {
  pinMode(analogPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  Serial.begin(9600);
}

void loop() {
  analogVal = analogRead(analogPin);
  if (millis() - past_time > 1000) {
    if (abs(past_analogVal - analogVal) > 3) {
      digitalWrite(ledPin, !digitalRead(ledPin));
      past_analogVal = analogVal;
      past_time = millis();
    }
  }
  delay(10);
}