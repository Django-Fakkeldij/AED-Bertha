
int x = 0;

#include <AccelStepper.h>  // Stepper driver library
// Dit zijn de pinnen die de Arduino gebruikt om de stappenmotoren aan te sturen
#define XSTEP 2
#define YSTEP 3
#define XDIR 5
#define YDIR 6
#define ENABLEPIN 8
#define STEPS (int)3200
#define MICROSTEPS 16
#define DEGREES (float)360
#define BAUDRATE 115200


int target_steps_1 = 0;
int target_steps_2 = 0;
bool isDone = true;
AccelStepper stepperX(1, XSTEP, XDIR);  // initialiseren van de stapper op poort x
AccelStepper stepperY(1, YSTEP, YDIR);  // initialiseren van de stapper op poort y
// AccelStepper stepperZ(1, ZSTEP, ZDIR);  // initialiseren van de stapper op poort z


void setup()  // Deze routine wordt 1 keer gerund aan het begin van het programma
{
  // Met pinMode zet je een pin op input/output
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(ENABLEPIN, OUTPUT);  // en ENABLEPIN(8) op output.
  // Met Serial kan je communiceren met de Serial monitor in Arduino IDE op je pc.
  Serial.begin(BAUDRATE);  // Gebruik dit commando eenmalig om de verbinding te maken.
  // Met digitalWrite kan je pinnen HIGH en LOW maken. Dit gebruiken we nu om de stappenmotoren in te schakelen.
  digitalWrite(ENABLEPIN, LOW);  // LOW= de motoren zijn actief. HIGH= de motoren zijn vrij te bewegen.
  // Tot slot laten we de led kort aangaan om te zien dat void setup() klaar is.
  digitalWrite(13, HIGH);
  digitalWrite(13, LOW);
  stepperX.setMaxSpeed(800);
  stepperY.setMaxSpeed(800);
  // stepperZ.setMaxSpeed(2000);
  stepperX.setAcceleration(3200);
  stepperY.setAcceleration(3200);
  // stepperZ.setAcceleration(4000);

  stepperX.moveTo(1600);  // De doelpositie in aantal stappen.
  stepperY.moveTo(1600);
}

void doBlink(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(200);
  }
}

void loop() {
  if (isDone && Serial.available()) {
    String target_steps_str = Serial.readString();
    int s = target_steps_str.indexOf(',');
    target_steps_1 = target_steps_str.substring(0, s).toInt();
    target_steps_2 = target_steps_str.substring(s + 1).toInt();

    isDone = false;
    Serial.print("Going to pos: ");
    Serial.print(target_steps_1);
    Serial.print(",");
    Serial.print(target_steps_2);
    Serial.flush();

    doBlink(2);  // Visual feedback, e.g., blink the LED
  }

  // Move steppers to target positions
  stepperX.moveTo(target_steps_1);  
  stepperY.moveTo(target_steps_2);

  // Keep running steppers until they reach the target
  while (stepperX.distanceToGo() != 0 || stepperY.distanceToGo() != 0) {
    stepperX.run();  
    stepperY.run();
  }

  // Check if both steppers have reached their final position
  if (!isDone && target_steps_1 == stepperX.currentPosition() && target_steps_2 == stepperY.currentPosition()) {
    isDone = true;
    
    // Send the "DONE" message when movement is complete
    Serial.println("DONE");
    Serial.flush();

    doBlink(4);  // Another visual feedback indicating completion
  }
}
