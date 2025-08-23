#include <DS1302.h>

const int CLK = 5;
const int DAT = 6;
const int RST = 7;

DS1302 myrtc(RST, DAT, CLK);

void setup()
{
  myrtc.halt(false);
  myrtc.writeProtect(false);

  Serial.begin(9600);
  Serial.println("DS1302RTC Test");
  Serial.println("----------------");

  myrtc.setDOW(MONDAY);
  myrtc.setTime(14, 30, 20);
  myrtc.setDate(13, 4, 2020);
}

void loop()
{
  Serial.print(myrtc.getDOWStr());
  Serial.print(" ");

  Serial.print(myrtc.getDateStr());
  Serial.print(" -- ");

  Serial.println(myrtc.getTimeStr());

  delay(1000);
}
