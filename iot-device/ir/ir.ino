#include <IRremote.h>  // IRremote 라이브러리 포함

void setup()
{
  // 디지털 12번 핀에 연결된 적외선 수신기 활성화
  IrReceiver.begin(12, ENABLE_LED_FEEDBACK);
  
  Serial.begin(9600); // 시리얼 통신 시작 (9600bps)
}

void loop()
{
  if (IrReceiver.decode()) // 신호가 수신되면
  {
    switch(IrReceiver.decodedIRData.command)
    {
      case 0x45:
        Serial.println("CH- button pressed");
        break;

      case 0x46:
        Serial.println("CH button pressed");
        break;

      case 0x47:
        Serial.println("CH+ button pressed");
        break;

      case 0x44:
        Serial.println("PREV button pressed");
        break;

      case 0x40:
        Serial.println("NEXT button pressed");
        break;

      case 0x43:
        Serial.println("PLAY/PAUSE button pressed");
        break;

      case 0x07:
        Serial.println("VOL- button pressed");
        break;

      case 0x15:
        Serial.println("VOL+ button pressed");
        break;

      case 0x09:
        Serial.println("EQ button pressed");
        break;

      case 0x16:
        Serial.println("0 button pressed");
        break;

      case 0x19:
        Serial.println("100+ button pressed");
        break;

      case 0x0D:
        Serial.println("200+ button pressed");
        break;

      case 0x0C:
        Serial.println("1 button pressed");
        break;

      case 0x18:
        Serial.println("2 button pressed");
        break;

      case 0x5E:
        Serial.println("3 button pressed");
        break;

      case 0x08:
        Serial.println("4 button pressed");
        break;

      case 0x1C:
        Serial.println("5 button pressed");
        break;

      case 0x5A:
        Serial.println("6 button pressed");
        break;

      case 0x42:
        Serial.println("7 button pressed");
        break;

      case 0x52:
        Serial.println("8 button pressed");
        break;

      case 0x4A:
        Serial.println("9 button pressed");
        break;
    }
    IrReceiver.resume(); // 다음 신호 대기
  }
}


