const byte messageBufSizeBytes = 32;
byte receivedBytes[messageBufSizeBytes];
byte numReceived = 0;
byte startMarker = 0x3C;
byte endMarker = 0x3E;

boolean newData = false;

int interval = 1000;
int lastTime = 0;

void setup() {
  Serial.begin(115200);
  Serial.print("<Arduino ready>");
}

void loop() {
  receiveMessage();
  int now = millis();
  if (now >= lastTime + interval) {

    // byte toSend[] = { 104, 101, 108, 108, 111 };
    // sendMessage(toSend, 5);

    lastTime = now;
  }

  if (newData) {
    byte toSend[] = { 104, 101, 108, 108, 111 };
    sendMessage(toSend, 5);
    newData = false;
  }
}

void receiveMessage() {
  // Here we will receive a message in the form of a byte array

  static boolean recvInProgress = false;
  static byte ndx = 0;
  byte rb;


  while (Serial.available() > 0 && newData == false) {
    rb = Serial.read();

    if (recvInProgress == true) {
      if (rb != endMarker) {
        receivedBytes[ndx] = rb;
        ndx++;
        if (ndx >= messageBufSizeBytes) {
          ndx = messageBufSizeBytes - 1;
        }
      } else {
        receivedBytes[ndx] = '\0';  // terminate the string
        recvInProgress = false;
        numReceived = ndx;  // save the number for use when printing
        ndx = 0;
        newData = true;
      }
    }

    else if (rb == startMarker) {
      recvInProgress = true;
    }
  }
}

void sendMessage(byte arr[], int size) {
  Serial.write(startMarker);
  Serial.write(arr, size);
  Serial.write(endMarker);
}