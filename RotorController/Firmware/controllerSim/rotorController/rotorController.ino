/*
 * Motor Controller Simulator
 * 
 * Nathan Thomas KI4HBD
 * thomasns@etsu.edu
 * 1/13/19
 * 
 *
 * Simulates a full motor controller on an arduino Uno
 * Allows testing without being connected to the full controller
 * Because my basement floor is cold
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

///////////////////////////////////
//Declarations for sim
// Counter and compare values
const uint16_t t1_load = 0;
const uint16_t t1_comp = 31250;
////////////////////////////////////

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

//////////////////////////////////////////
  // Set up timer interrupt for the simulator
  // Reset Timer1 Control Reg A
  TCCR1A = 0;

  // Set to prescaler of 256
  TCCR1B |= (1 << CS12);
  TCCR1B &= ~(1 << CS11);
  TCCR1B &= ~(1 << CS10);
    // Reset Timer1 and set compare value
  TCNT1 = t1_load;
  OCR1A = t1_comp;

  // Enable Timer1 overflow interrupt
  TIMSK1 = (1 << OCIE1A);

  // Enable global interrupts
  sei();
//////////////////////////////////////////
  
  Serial.print("Reactor Online\nSensors online\nAll Systems Nominal\n"); //we're alive. 
}

void loop() {

  checkMotors(); //See if we need to stop motion
  
  if (Serial.available() > 0) { //Look for new commands
    // read the incoming byte:
    String s = Serial.readStringUntil('\n');
    parse(s);
  }
}

//Parse the command and run it
void parse(String command) {
  //We won't have many commands to worry about so we'll do this sloppily 
  if(command.startsWith("move")) {
    //move commands will be formated "MOVE MM D Steps" Where MM is the motor (EL/AZ) and D is the direction (P/N)
    //split at 0-4, 5-6, 8, 10-END
    String motor = command.substring(5,7);
    String dir = command.substring(8,9);
    int steps = command.substring(10).toInt();

    driveMotor(motor, dir, steps);
    
  }
  else
    Serial.println("WARNING:INVALID UNKNOWN");
}


void driveMotor(String Motor, String dir, int steps) {
  if(Motor == "AZ") {
    if(!AZMoving){ //only attempt to move if the motor isn't already moving
      Serial.println("STARTED:AZ");
      AZMoving = true;
      AZStepsLeft = steps;
      digitalWrite(AZ_PWM,HIGH);
    }
    else 
      Serial.println("WARNING:RUNNING AZ");
  }
  else if(Motor == "EL") {
    if(!ELMoving){ //only attempt to move if the motor isn't already moving
      Serial.println("STARTED:EL");
      ELMoving = true;
      ELStepsLeft = steps;
      digitalWrite(EL_PWM,HIGH);
    }
    else 
      Serial.println("WARNING:RUNNING EL");
  }

    
}

void checkMotors() {
  //check motor movement
  if(AZMoving) { //only check if in motion
    if(AZStepsLeft <= 0) { //if we've reached the desired number of Steps
      AZStepsLeft = 0;
      AZMoving = false;
      digitalWrite(AZ_PWM,LOW);
      Serial.println("STOPPED:AZ");
    }
    
  }
  if(ELMoving) {
    if(ELStepsLeft <= 0){
      ELStepsLeft = 0;
      ELMoving = false;
      digitalWrite(EL_PWM,LOW);
      Serial.println("STOPPED:EL");
    }   
  }

}

void AZPulse() {

  if(millis() - AZLastPulse > 200) {
  AZStepsLeft--;
  AZLastPulse = millis();
  Serial.println("STEPPED:AZ");
  }
}

void ELPulse() {
  if(millis() - ELLastPulse > 200) {
    ELStepsLeft--;  
    ELLastPulse = millis();
    Serial.println("STEPPED:EL");
  }
}


///////////////////
// Interrupt for sim
ISR(TIMER1_COMPA_vect) {
  TCNT1 = t1_load;
  if(AZMoving)
    AZPulse();
  if(ELMoving)
    ELPulse();
}
////////////////////
