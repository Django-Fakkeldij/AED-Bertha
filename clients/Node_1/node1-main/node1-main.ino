#include <AccelStepper.h>  // Stepper driver library
#include <cppQueue.h>      // FIFO Queue lib

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
#define QUEUE_LENGTH 10

// BEGIN COMM LIB
const byte messageBufSizeBytes = 32;
byte receivedBytes[messageBufSizeBytes];
byte numReceived = 0;
byte startMarker = 0x3C;
boolean shouldReceiveNewMessage = false;

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

  while (Serial.available() > 0 && shouldReceiveNewMessage == false) {

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
        shouldReceiveNewMessage = true;
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
  uint16_t motor2_steps;
} stepsPositionRec;

cppQueue q(sizeof(stepsPositionRec), QUEUE_LENGTH);

stepsPositionRec current = { 0, 0 };
bool isDoneWithNextMove = true;
bool requestedNewValue = false;


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
  stepperX.setMaxSpeed(1600);
  stepperY.setMaxSpeed(1600);
  stepperX.setAcceleration(6400);
  stepperY.setAcceleration(6400);

  startMessageProto();
}

void loop() {
  receiveMessage();

  if (!q.isFull() && !requestedNewValue) {

    // Queue is not full, therefore request more values
    byte toSend[] = { 68, 79, 78, 69 };
    sendMessage(toSend, sizeof(toSend));

    // Flag that a new value has already been requested
    requestedNewValue = true;
    
    // Flag that a new message should be read
    shouldReceiveNewMessage = true;
  }

  // Ready to decode new positions when new data arrived
  if (shouldReceiveNewMessage) {
    stepsPositionRec newRecord;
    newRecord.motor1_steps = (int32_t)receivedBytes[0] | (int32_t)(receivedBytes[1] << 8) | (int32_t)(receivedBytes[2] << 16) | (int32_t)(receivedBytes[3] << 24);
    newRecord.motor1_steps = newRecord.motor1_steps - 3200;
    newRecord.motor2_steps = (int32_t)receivedBytes[4] | (int32_t)(receivedBytes[5] << 8) | (int32_t)(receivedBytes[6] << 16) | (int32_t)(receivedBytes[7] << 24);
    newRecord.motor2_steps = newRecord.motor2_steps - 3200;

    // Add new record to the queue
    q.push(&newRecord);

    // new message had been received
    shouldReceiveNewMessage = false;
    // a new message can be requested
    requestedNewValue = false;
  }

  // Move steppers to target positions
  stepperX.moveTo(current.motor1_steps);
  stepperY.moveTo(current.motor2_steps);


  // TODO: while and if statement can probably be combined ?
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

  // Detect if next move can be executed and if so, where to
  if (isDoneWithNextMove) {
    q.pop(&current);
    isDoneWithNextMove = false;
  }
}
