#include <Wire.h>
#include <INA3221.h>
#include <ServoTimer2.h>

#define BAUDRATE 115200

const int buttonPin = 2;
const int servoPin = 9;
const int enB = 10;
const int dir1 = 11;
const int dir2 = 12;
const int ledPin = 13;

unsigned long timeMillis;           // Voor het bijhouden van de tijd
unsigned long nextMeasurement = 0;  //Tijd voor het volgende meetpunt
unsigned long sampleRate = 25;      //Interval tussen de meetpunten
unsigned long sendIsDone = 0;

float current1;        //Ruwe meetwaardes
float current1S;       //'Smooth' meetwaardes
float current1Val[8];  //5 meetwaardes om gemiddelde mee te berekenen

float current2;
float current2S;
float current2Val[8];

int targetPos = 80;

bool screwin = false;
bool screwout = false;
bool moveup = false;
bool movedown = false;

int message = 0;
bool isDoneWithNextMove = false;

INA3221 ina3221(INA3221_ADDR40_GND);
ServoTimer2 zServo;





// BEGIN COMM LIB
const byte messageBufSizeBytes = 32;
byte receivedBytes[messageBufSizeBytes];
byte numReceived = 0;
byte startMarker = 0x3C;
boolean shouldParseNewMessageAndNotReceiveNewMessage = false;
bool processed_message = false;


int interval = 1000;
int lastTime = 0;

void blink(int n, int interval = 500) {
  for (int i = 0; i < n; i++) {
    digitalWrite(ledPin, HIGH);  // turn the LED on (HIGH is the voltage level)
    delay(interval);             // wait for a second
    digitalWrite(ledPin, LOW);   // turn the LED off by making the voltage LOW
    delay(interval);             // wait for a second
  }
}

void startMessageProto() {
  Serial.begin(BAUDRATE);
  pinMode(ledPin, OUTPUT);
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

  while (Serial.available() > 0 && shouldParseNewMessageAndNotReceiveNewMessage == false) {

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
        shouldParseNewMessageAndNotReceiveNewMessage = true;
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





// START CONTROL
float currentSmoothing(float currentiVal[8], float currenti) {

  float currentiS = 0.0;

  //Alle waarden in de array een plek doorschuiven en nieuwe meetwaarde op plek 0 zetten
  for (int i = 7; i >= 0; i--) {
    if (i != 0) {
      currentiVal[i] = currentiVal[i - 1];
    } else {
      currentiVal[i] = currenti;
    }
  }

  //Alle waarden in array bij elkaar optellen en delen door 5 om het gemiddelde te krijgen
  for (int i = 0; i < 8; i++) {
    currentiS += currentiVal[i];
  }
  currentiS = currentiS / 8;

  return currentiVal, currentiS;
}

int position(int angle) {

  //Pulse lengte uitreken op basis van een hoek (range 500-2500 us, 0-180 graden), nodig voor ServoTimer2.h
  if (angle >= 0 && angle <= 180) {
    return int(500 + (angle * 11.11));  //min pulsewidth = 500, max 2500. Formula pulsewidth = 500 + 180/2000 * angle (=*11.11)
  }
}

void screwIn() {

  //Richting 1 draaien
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, LOW);
  analogWrite(enB, 255);  //const speed 200/255 * 12 ~ 9.5v

  if (targetPos < 110) {
    targetPos = 110;
  }

  //Constante druk van servo
  if ((current2S < 35 && current2S > 0) && targetPos < 155) {  //Zet deze omhoog voor meer neerwaartse druk van de servo
    targetPos += 1;
  } else if (current2S >= 75 && targetPos > 80) {  //Zet deze omhoog voor minder snel terug bewegen van de servo
    targetPos -= 1;
  }

  //Stopcondities
  if ((current1S >= 265 && targetPos > 140) || targetPos >= 155 || (current1S < 30 && targetPos >= 130)) {  //Zet current omhoog voor hoger aandraaimoment
    screwin = false;
    digitalWrite(dir1, LOW);
    isDoneWithNextMove = true;
  }
}

void screwOut() {

  //Richting 2 draaien
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, HIGH);

  analogWrite(enB, 255);  //const speed 200/255 * 12 ~ 9.5v


  //Constante druk van servo
  if ((current1S > -180 && current1S <= 0) && (targetPos > 130 && targetPos <= 155) && current2S < 35) {  //Zet deze omhoog voor minder snel terug bewegen van de servo
    targetPos += 1;
  } else if (((current2S >= 25 && current1S < -80) || current2S > 120 || current1S < -150) && targetPos > 80) {  //Zet de current omhoog voor meer tegendruk tijdens het losschroeven
    targetPos -= 1;
  } else if (current1S > 0 && targetPos < 130) {  //stall
    targetPos -= 1;
  }


  if (targetPos <= 130 && targetPos > 110) {
    targetPos -= 1;
  }

  //Stopcondities
  if (targetPos <= 110) {
    screwout = false;
    targetPos = 80;
    digitalWrite(dir2, LOW);
    isDoneWithNextMove = true;
  }
}

void moveUp() {
  targetPos = 80;
  moveup = false;
  zServo.write(position(targetPos));
  delay(100);
  isDoneWithNextMove = true;
}

void moveDown() {
  targetPos = 138;
  movedown = false;
  zServo.write(position(targetPos));
  delay(200);
  isDoneWithNextMove = true;
}

// END CONTROL





void setup()  // Deze routine wordt 1 keer gerund aan het begin van het programma
{
  startMessageProto();


  pinMode(enB, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);

  zServo.attach(servoPin);

  ina3221.begin();
  ina3221.reset();
  ina3221.setShuntRes(100, 100, 100);

  // Note that isDoneWithNextMove will be set to true when a command is called. Otherwise it will not start receiving values.
  // moveUp();
}





void loop() {

  receiveMessage();
  // Ready to decode new positions when new data arrived

  // Recieving new data
  if (shouldParseNewMessageAndNotReceiveNewMessage) {
    message = (int32_t)receivedBytes[0] | (int32_t)(receivedBytes[1] << 8) | (int32_t)(receivedBytes[2] << 16) | (int32_t)(receivedBytes[3] << 24);
    if (!processed_message) {
      switch (message) {
        case 0:
          break;
        case 1111:
          isDoneWithNextMove = false;
          screwin = true;
          processed_message = true;
          break;
        case 2222:
          isDoneWithNextMove = false;
          screwout = true;
          processed_message = true;
          break;
        case 3333:
          isDoneWithNextMove = false;
          moveup = true;
          processed_message = true;
          break;
        case 4444:
          isDoneWithNextMove = false;
          movedown = true;
          processed_message = true;
          break;
        default:  // Ontvangen data niet goed, error
          blink(3, 500);
          break;
      }
    }
  }

  if (isDoneWithNextMove && shouldParseNewMessageAndNotReceiveNewMessage) {
    shouldParseNewMessageAndNotReceiveNewMessage = false;
    // blink(3);

    // Signal done
    byte toSend[] = { 68, 79, 78, 69 };
    sendMessage(toSend, sizeof(toSend));
    isDoneWithNextMove = false;
    processed_message = false;
  }
  //end recieving new data



  //control
  timeMillis = millis();

  if (timeMillis >= nextMeasurement) {  //every 25 ms

    //Uitlezen CH1 & CH2 van de INA3221
    current1 = ina3221.getCurrent(INA3221_CH1) * 1000;
    current2 = ina3221.getCurrent(INA3221_CH2) * 1000;

    //Error lampje als er geen stroom loopt
    if (current1 == 0.0 && current2 == 0.0) digitalWrite(ledPin, HIGH);
    else digitalWrite(ledPin, LOW);

    //Smoothing door een gemmiddelde te pakken van 5 meetwaardes
    current1Val, current1S = currentSmoothing(current1Val, current1);
    current2Val, current2S = currentSmoothing(current2Val, current2);

    if (screwin) screwIn();
    else if (screwout) screwOut();
    else if (movedown) moveDown();
    else if (moveup) moveUp();

    if ((current1 == 0.0 && current2 == 0.0) || (targetPos < 0 && targetPos > 180)) digitalWrite(ledPin, HIGH);
    else digitalWrite(ledPin, LOW);

    if (targetPos >= 0 && targetPos <= 180) zServo.write(position(targetPos));

    nextMeasurement = timeMillis + sampleRate;
  }
}
