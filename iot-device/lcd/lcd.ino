#include <LiquidCrystal.h>

LiquidCrystal lcd(4, 5, 8, 9, 10, 11);   // (RS, E, DB4,DB5,DB6,DB7)

void setup() {
  lcd.begin(16, 2);
}

void loop() {
  lcd.setCursor(1, 0);        // 2열, 1행부터 출력
  lcd.print("Hello");         // 'Hello'
  lcd.setCursor(4, 1);        // 5열, 2행부터 출력
  lcd.print("Eduino!");       // 'Eduino'
  delay(1000);                // 1초대기
  lcd.clear();                // LCD 문자열 삭제

  lcd.setCursor(0, 0);        // 1열, 1행부터 출력
  lcd.print("www.eduino.kr"); // 'www.eduino.kr'
  delay(1000);                // 1초대기
  lcd.clear();                // LCD 문자열 삭제
}// 테스트

