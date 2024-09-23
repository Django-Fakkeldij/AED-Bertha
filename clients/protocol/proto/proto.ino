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




void setup() {
  startMessageProto();
}

void loop() {
  receiveMessage();
  int now = millis();
  if (now >= lastTime + interval) {

    lastTime = now;
  }


  if (newData) {
    sendMessage(receivedBytes, messageBufSizeBytes);
    newData = false;
  }
}
