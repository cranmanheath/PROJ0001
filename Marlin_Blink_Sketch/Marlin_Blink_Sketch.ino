const int ledPin =  27;
int ledState = LOW;
long previousMillis = 0;
long interval = 1000;

void setup() {
  pinMode(ledPin, OUTPUT);     
}

void loop()
{
  unsigned long currentMillis = millis();
 
  if(currentMillis - previousMillis > interval) {
    previousMillis = currentMillis;  
    if (ledState == LOW)
      ledState = HIGH;
    else
      ledState = LOW;
    digitalWrite(ledPin, ledState);
  }
}
