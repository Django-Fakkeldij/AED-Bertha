#include <AccelStepper.h>  // Stepper driver library
#include <cppQueue.h>      // FIFO Queue lib

// Dit zijn de pinnen die de Arduino gebruikt om de stappenmotoren aan te sturen
#define XSTEP 2
#define YSTEP 3
#define XDIR 5
#define YDIR 6
#define ENABLEPIN 8
#define MICROSWITCHPINX 9
#define MICROSWITCHPINY 10
#define STEPS (int)3200
#define MICROSTEPS 16
#define DEGREES (float)360
#define BAUDRATE 115200

// BEGIN COMM LIB
const byte messageBufSizeBytes = 32;
byte receivedBytes[messageBufSizeBytes];
byte numReceived = 0;
byte startMarker = 0x3C;
boolean shouldParseNewMessage = false;

int interval = 1000;
int lastTime = 0;

void blink(int n, int interval = 500) {
  for (int i = 0; i < n; i++) {
    digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
    delay(interval);                  // wait for a second
    digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
    delay(interval);                  // wait for a second
  }
}

void startMessageProto() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  byte toSend[] = { 104, 101, 108, 108, 111 };
  sendMessage(toSend, 5);
}

void receiveMessage() {
  // Here we will receive a message in the form of a byte array

  static boolean recvInProgress = false;
  static byte ndx = 0;
  static byte mes_len = 0;
  static bool read_length = false;
  byte rb;

  while (Serial.available() > 0 && shouldParseNewMessage == false) {

    rb = Serial.read();

    if (read_length) {
      mes_len = rb;
      read_length = false;
    } else if (recvInProgress == true) {
      receivedBytes[ndx] = rb;
      ndx++;
      if (ndx >= messageBufSizeBytes) {
        ndx = messageBufSizeBytes - 1;
      }
      if (ndx >= mes_len) {

        receivedBytes[ndx] = '\0';  // terminate the string
        recvInProgress = false;
        numReceived = ndx;  // save the number for use when printing
        ndx = 0;
        shouldParseNewMessage = true;
        mes_len = 0;
      }
    } else if (rb == startMarker) {
      recvInProgress = true;
      read_length = true;
    }
  }
}

void sendMessage(byte arr[], byte size) {
  Serial.write(startMarker);
  Serial.write(size);
  Serial.write(arr, size);
}
// END COMM LIB

// stepsPositionRecord
typedef struct stepsPositionRec {
  uint32_t motor1_steps;
  uint32_t motor2_steps;
} stepsPositionRec;


bool isDoneWithNextMove = true;
stepsPositionRec current = { 0, 0 };



AccelStepper stepperX(1, XSTEP, XDIR);  // initialiseren van de stapper op poort x
AccelStepper stepperY(1, YSTEP, YDIR);  // initialiseren van de stapper op poort y

int homing_offsetX = 0;
int homing_offsetY = 0;


void setup()  // Deze routine wordt 1 keer gerund aan het begin van het programma
{
  // MOTOR SETUP
  pinMode(ENABLEPIN, OUTPUT);  // en ENABLEPIN op output.
  // Met digitalWrite kan je pinnen HIGH en LOW maken. Dit gebruiken we nu om de stappenmotoren in te schakelen.
  digitalWrite(ENABLEPIN, LOW);  // LOW= de motoren zijn actief. HIGH= de motoren zijn vrij te bewegen.

  pinMode(LED_BUILTIN, OUTPUT);
  // blink(10);

  // MICROSWITCH SETUP
  pinMode(MICROSWITCHPINX, INPUT_PULLUP);
  pinMode(MICROSWITCHPINY, INPUT_PULLUP);
  int switchX = digitalRead(MICROSWITCHPINX);
  int switchY = digitalRead(MICROSWITCHPINY);


  // ------------------------------------

  homing_offsetX = -150;
  homing_offsetY = -150;

  stepperX.setMaxSpeed(8192 * 2);
  stepperY.setMaxSpeed(8192 * 2);
  stepperX.setAcceleration(8192 * 2);
  stepperY.setAcceleration(8192 * 2);
  stepperX.runToNewPosition(homing_offsetX);
  stepperY.runToNewPosition(homing_offsetY);

  while (digitalRead(MICROSWITCHPINX) == HIGH) {
    homing_offsetX = homing_offsetX + 1;
    stepperX.runToNewPosition(homing_offsetX);
  }
  while (digitalRead(MICROSWITCHPINY) == HIGH) {
    // while (true) {
    homing_offsetY = homing_offsetY + 1;
    stepperY.runToNewPosition(homing_offsetY);
  }

  homing_offsetX = -50 + homing_offsetX;
  homing_offsetY = -50 + homing_offsetY;

  stepperX.setMaxSpeed(512);
  stepperY.setMaxSpeed(512);
  stepperX.setAcceleration(512);
  stepperY.setAcceleration(512);
  stepperX.runToNewPosition(homing_offsetX);
  stepperY.runToNewPosition(homing_offsetY);

  while (digitalRead(MICROSWITCHPINX) == HIGH) {
    homing_offsetX = homing_offsetX + 1;
    stepperX.runToNewPosition(homing_offsetX);
  }
  while (digitalRead(MICROSWITCHPINY) == HIGH) {
    // while (true) {
    homing_offsetY = homing_offsetY + 1;
    stepperY.runToNewPosition(homing_offsetY);
  }

  stepperX.setMaxSpeed(40 * 1000);
  stepperY.setMaxSpeed(40 * 1000);
  stepperX.setAcceleration(10 * 1000);
  stepperY.setAcceleration(10 * 1000);


  startMessageProto();
}

void loop() {
  receiveMessage();
  // Ready to decode new positions when new data arrived
  if (shouldParseNewMessage) {
    stepsPositionRec newRecord;
    newRecord.motor1_steps = (int32_t)receivedBytes[0] | (int32_t)(receivedBytes[1] << 8) | (int32_t)(receivedBytes[2] << 16) | (int32_t)(receivedBytes[3] << 24);
    newRecord.motor1_steps = newRecord.motor1_steps - 3200;
    newRecord.motor2_steps = (int32_t)receivedBytes[4] | (int32_t)(receivedBytes[5] << 8) | (int32_t)(receivedBytes[6] << 16) | (int32_t)(receivedBytes[7] << 24);
    newRecord.motor2_steps = newRecord.motor2_steps - 3200;
    current = newRecord;

  }

  // Move steppers to target positions
  stepperX.moveTo(current.motor1_steps + homing_offsetX);
  stepperY.moveTo(current.motor2_steps + homing_offsetY);

  // Keep running steppers until they reach the target
  while (stepperX.distanceToGo() != 0 || stepperY.distanceToGo() != 0) {
    isDoneWithNextMove = false;
    stepperX.run();
    stepperY.run();
  }

  // Check if both steppers have reached their final position
  if (stepperX.distanceToGo() == 0 && stepperY.distanceToGo() == 0) {
    isDoneWithNextMove = true;
  } else {
    isDoneWithNextMove = false;
  }

  if (isDoneWithNextMove && shouldParseNewMessage) {
    shouldParseNewMessage = false;
    // Signal done
    byte toSend[] = { 68, 79, 78, 69 };
    sendMessage(toSend, sizeof(toSend));
    isDoneWithNextMove = false;
  }
}
