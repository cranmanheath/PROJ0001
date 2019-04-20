#include <Servo.h>
int pcCommand;

int lightpin_1 = 1;

void setup() {
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  if(Serial.available() > 0){
    pcCommand = Serial.read();
    //Serial.println(pcCommand);
    switch(pcCommand){
      case '1':  //status check
        Serial.println("ok");
        break;
      case '2':  //read light value
        Serial.println(analogRead(lightpin_1));
        Serial.println("ok");
        break;
    }
  }
}
