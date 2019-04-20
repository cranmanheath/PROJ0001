#include <Servo.h>
int pcCommand;

//Servo servo_1; 
//Servo servo_2;

//int servopin_1 = 9;
//int servopin_2 = 10;

//int servopos_1 = 90;  //servo 1 position variable
//int servopos_2 = 90;  //servo 2 position variable

int lightpin_1 = 1;
//int lightpin_2 = 2;
//int lightpin_3 = 3;
//int lightpin_4 = 4;

void setup() {
  Serial.begin(9600);
//  servo_1.attach(servopin_1);
//  servo_1.write(servopos_1);
  
//  servo_2.attach(servopin_2);
//  servo_2.write(servopos_2);
}

// the loop routine runs over and over again forever:
void loop() {
  if(Serial.available() > 0){
    pcCommand = Serial.read();
    switch(pcCommand){
      case 1:  //status check
        Serial.println("ok");
      case 2:  //read light value
        Serial.println(analogRead(lightpin_1));
        Serial.println("ok");
    }
  }
//   Serial.println(analogRead(lightpin_1));
//   Serial.println('ok');
// }  
// else{
//   Serial.println(""); 
// }
 
// Serial.print(analogRead(lightpin_1)); 
// Serial.print("  ");
// Serial.print(analogRead(lightpin_2));
// Serial.print("  ");
// Serial.print(analogRead(lightpin_3));
// Serial.print("  ");
// Serial.println(analogRead(lightpin_4));
// delay(25);
// move_left_right();
// move_up_down();
}


//void move_left_right(){
// if (analogRead(lightpin_1) - analogRead(lightpin_2) > 40 ){
//   servo_1.write(servopos_1 +=1);
//   delay(15);
// }
// else if (analogRead(lightpin_1) - analogRead(lightpin_2) < -40 ){
//   servo_1.write(servopos_1 -=1);
//   delay(15);
// }
//} 


//void move_up_down(){
//  if (analogRead(lightpin_3) - analogRead(lightpin_4) > 20 ){
//   servo_2.write(servopos_2 +=1);
//   delay(15);
// }
// else if (analogRead(lightpin_3) - analogRead(lightpin_4) < -20 ){
//   servo_2.write(servopos_2 -=1);
//   delay(15);
// }
//} 
