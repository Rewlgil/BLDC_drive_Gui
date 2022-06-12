void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(10);
  pinMode(13, OUTPUT);
}

void loop()
{
  if (Serial.available() > 0)
  {
    Serial.readStringUntil("\n");
    digitalWrite(13, !digitalRead(13));
  }
}
