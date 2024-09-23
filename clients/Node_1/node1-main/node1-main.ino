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

// BEGIN COMM LIB
const byte messageBufSizeBytes = 32;
byte receivedBytes[messageBufSizeBytes];
byte numReceived = 0;
byte startMarker = 0x3C;
boolean newData = false;

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

  while (Serial.available() > 0 && newData == false) {

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
        newData = true;
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


int target_steps_1 = 0;
int target_steps_2 = 0;
bool isDone = true;
AccelStepper stepperX(1, XSTEP, XDIR);  // initialiseren van de stapper op poort x
AccelStepper stepperY(1, YSTEP, YDIR);  // initialiseren van de stapper op poort y


void setup()  // Deze routine wordt 1 keer gerund aan het begin van het programma
{
  pinMode(ENABLEPIN, OUTPUT);  // en ENABLEPIN(8) op output.
  // Met digitalWrite kan je pinnen HIGH en LOW maken. Dit gebruiken we nu om de stappenmotoren in te schakelen.
  digitalWrite(ENABLEPIN, LOW);  // LOW= de motoren zijn actief. HIGH= de motoren zijn vrij te bewegen.
  // Tot slot laten we de led kort aangaan om te zien dat void setup() klaar is.
  digitalWrite(13, HIGH);
  digitalWrite(13, LOW);
  stepperX.setMaxSpeed(800);
  stepperY.setMaxSpeed(800);
  stepperX.setAcceleration(6400);
  stepperY.setAcceleration(6400);

  startMessageProto();
}

void loop() {
  receiveMessage();
  // Ready to decode new positions when new data arrived
  if (newData) {
    target_steps_1 = (int32_t)receivedBytes[0] | (int32_t)(receivedBytes[1] << 8) | (int32_t)(receivedBytes[2] << 16) | (int32_t)(receivedBytes[3] << 24);
    target_steps_1 = target_steps_1 - 3200;
    target_steps_2 = (int32_t)receivedBytes[4] | (int32_t)(receivedBytes[5] << 8) | (int32_t)(receivedBytes[6] << 16) | (int32_t)(receivedBytes[7] << 24);
    target_steps_2 = target_steps_2 - 3200;
  }

  // Move steppers to target positions
  stepperX.moveTo(target_steps_1);
  stepperY.moveTo(target_steps_2);

  // Keep running steppers until they reach the target
  while (stepperX.distanceToGo() != 0 || stepperY.distanceToGo() != 0) {
    isDone = false;
    stepperX.run();
    stepperY.run();
  }

  // Check if both steppers have reached their final position
  if (stepperX.distanceToGo() == 0 && stepperY.distanceToGo() == 0) {
    isDone = true;
  } else {
    isDone = false;
  }

  if (isDone && newData) {
    newData = false;
    // Signal done
    byte toSend[] = { 68, 79, 78, 69 };
    sendMessage(toSend, sizeof(toSend));
    isDone = false;
  }
}
