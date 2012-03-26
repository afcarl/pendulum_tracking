#include <Servo.h> 
 
Servo servoYaw;
Servo servoPitch;

int pos = 0;    
 
void setup() 
{ 
  servoPitch.attach(9);
  servoYaw.attach(10);  
  servoYaw.write(90);
  servoPitch.write(90);
  Serial.begin(19200);
  Serial.println("Receiving commands.");
} 

void loop() 
{ 
  static int buffer = 0;

  if (Serial.available())
  {
    char ch = Serial.read();

    switch(ch)
    {
      case '0'...'9':
        buffer = buffer * 10 + ch - '0';
        break;
      case 's':
        servoYaw.write(buffer);
        delay(15);
        //Serial.print("Yaw is set to: ");
        //Serial.print(buffer, DEC);
        //Serial.println(" degrees");
        buffer = 0;
        break;
      case 't':
        servoPitch.write(buffer);
        delay(15);
        //Serial.print("Pitch is set to: ");
        //Serial.print(buffer, DEC);
        //Serial.println(" degrees");
        buffer = 0;
        break;
    }
  }
} 
