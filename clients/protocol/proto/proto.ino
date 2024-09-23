const byte messageBufSizeBytes = 32;
byte receivedBytes[messageBufSizeBytes];
byte numReceived = 0;
byte startMarker = 0x3C;
byte endMarker = 0x3E;

boolean newData = false;

int interval = 1000;
int lastTime = 0;

void blink(int n) {
  for (int i = 0; i < n; i++) {
    digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
    delay(1000);                      // wait for a second
    digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
    delay(1000);                      // wait for a second
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  // Serial.print("<Arduino ready>");
}

void loop() {
  // receiveMessage();
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
  static byte mes_len = 0;
  byte rb;


  while (Serial.available() > 0 && newData == false) {
    rb = Serial.read();



    if (recvInProgress == true) {
      if (mes_len == 0) {
        mes_len = rb;
        blink(mes_len);
      } else if (ndx != mes_len - 1) {
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
        mes_len = 0;
      }
    } else if (rb == startMarker) {
      recvInProgress = true;
    }
  }
}

void sendMessage(byte arr[], byte size) {
  Serial.write(startMarker);
  Serial.write(size);
  Serial.write(arr, size);
}