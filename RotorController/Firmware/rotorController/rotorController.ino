/*
 * New SRT Motor Controller Firmware
 * 
 * Nathan Thomas KI4HBD
 * thomasns@etsu.edu
 * 10/15/18 
 * 
 * This is the firmware for the updated radio telescope motor controller. 
 * Please note this is just a basic test at the moment and doesnt do anything useful.
 * Based on the MIT SRT 
 *  
 */

int AZ_PULSE = 3; //interrupt pin for reading the AZ reed switch
int EL_PULSE = 2;//interrupt pin for reading the EL reed switch
int AZ_DIR = 8; //pin for controlling the AZ direction
int EL_DIR = 9; //pin for controlling the EL direction 
int AZ_PWM = 5; //pin for controlling the AZ HBridge
int EL_PWM = 6; //pin for controlling the EL HBridge

bool AZMoving; // is the AZ motor currently moving
bool ELMoving;// is the EL motor currently moving
int AZStepsLeft; //how many steps the AZ has left to move
int ELStepsLeft; //how many steps the EL has left to move

unsigned long AZLastPulse; //used to debounce the AZ Pulse line
unsigned long ELLastPulse; //used to debounce the EL Pulse line


void setup() {
  // put your setup code here, to run once:
  
  //Setup pins and interrupts
  pinMode(AZ_PULSE,INPUT);
  pinMode(EL_PULSE,INPUT);
  pinMode(AZ_DIR, OUTPUT);
  digitalWrite(AZ_DIR,LOW);
  pinMode(EL_DIR, OUTPUT);
  digitalWrite(EL_DIR,LOW);
  pinMode(AZ_PWM, OUTPUT);
  digitalWrite(AZ_PWM,LOW);
  pinMode(EL_PWM, OUTPUT);
  digitalWrite(EL_PWM,LOW);
  attachInterrupt(digitalPinToInterrupt(AZ_PULSE), AZPulse, FALLING);
  attachInterrupt(digitalPinToInterrupt(EL_PULSE), ELPulse, FALLING);
  AZLastPulse = millis();
  ELLastPulse = millis();

  AZMoving = false;
  ELMoving = false;
  
  //Setup serial communications
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.print("Reactor Online\nSensors online\nAll Systems Nominal\n"); //we're alive. 
}

void loop() {

  checkMotors(); //See if we need to stop motion
  
  if (Serial.available() > 0) { //Look for new commands
    // read the incoming byte:
    String s = Serial.readString();
    parse(s);
  }
}

//Parse the command and run it
void parse(String command) {

  //We won't have many commands to worry about so we'll do this sloppily 
  if(command.startsWith("move")) {
    Serial.print("move command received\n");
    //move commands will be formated "MOVE MM D Steps" Where MM is the motor (EL/AZ) and D is the direction (P/N)
    //split at 0-4, 5-6, 8, 10-END
    String motor = command.substring(5,7);
    String dir = command.substring(8,9);
    int steps = command.substring(10).toInt();

    driveMotor(motor, dir, steps);
    
  }
  else
    Serial.print("invalid command");
}


void driveMotor(String Motor, String dir, int steps) {
  if(Motor == "AZ") {
    if(!AZMoving){ //only attempt to move if the motor isn't already moving
      Serial.print("Moving Azmith " + String(steps) + " steps in the " + String(dir) + " direction\n");
      AZMoving = true;
      AZStepsLeft = steps;
      digitalWrite(AZ_PWM,HIGH);
    }
    else 
      Serial.print("Azmith is already moving, ignoring command\n");
  }
  else if(Motor == "EL") {
    if(!ELMoving){ //only attempt to move if the motor isn't already moving
      Serial.print("Moving Elevation  " + String(steps) + " steps in the " + String(dir) + " direction\n");
      ELMoving = true;
      ELStepsLeft = steps;
      digitalWrite(EL_PWM,HIGH);
    }
    else 
      Serial.print("Elivation is already moving, ignoring command\n");
  }

    
}

void checkMotors() {
  //check motor movement
  if(AZMoving) { //only check if in motion
      if(millis() % 100  < 20)
    Serial.print("Azmith steps left: " + String(AZStepsLeft) + "\n");
    if(AZStepsLeft <= 0) { //if we've reached the desired number of Steps
      Serial.print("Azmith steps left: " + String(AZStepsLeft) + "\n");
      AZStepsLeft = 0;
      AZMoving = false;
      digitalWrite(AZ_PWM,LOW);
    }
    
  }
  if(ELMoving) {
    if(ELStepsLeft <= 0){
      if(millis() % 100  < 20)
        Serial.print("Elevation steps left: " + String(ELStepsLeft) + "\n");
      ELStepsLeft = 0;
      ELMoving = false;
      digitalWrite(EL_PWM,LOW);
    }   
  }

}

void AZPulse() {
  if(millis() - AZLastPulse < 200)
    AZStepsLeft--;
  AZLastPulse = millis();
}

void ELPulse() {
  if(millis() - ELLastPulse < 200)
    ELStepsLeft--;  
  ELLastPulse = millis();
}
