void setup()
{
  Serial.begin(1000000);
  Serial.setTimeout(10);
  pinMode(13, OUTPUT);
}

String msg;

void loop()
{
  if (Serial.available() > 0)
  {
    msg = Serial.readStringUntil('\n');
    Serial.println(msg);
    digitalWrite(13, !digitalRead(13));
  }
}
