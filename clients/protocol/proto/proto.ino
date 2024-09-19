#define BAUDRATE 115200


void serialClear() {
  // (Bits - 1 for endbit) / 8 = bytes per sec => 1000 / bytes per sec = time to wait for each byte
  // int time_to_wait = 1000 / ((BAUDRATE - (BAUDRATE / 9)) / 8);
  // Margin in ms
  int margin = 5;
  while (Serial.available() > 0) {
    char t = Serial.read();
    delay(margin);
  }
}

void waitForBytes(int x) {
  while (Serial.available() < x) {
  }
}



void setup() {
  Serial.begin(BAUDRATE);  // Gebruik dit commando eenmalig om de verbinding te maken.
}

void loop() {
  waitForBytes(12);
  String a = Serial.readString();
  Serial.println(a);
  serialClear();

  // int start_byte = Serial.parseInt();
  // int another_start_byte = Serial.parseInt();
  // int command = Serial.parseInt();
  // int args_len = Serial.parseInt();
  // serialClear();
  // Serial.println("Got the following data: ");
  // Serial.println(start_byte);
  // Serial.println(another_start_byte);
  // Serial.println(command);
  // Serial.println(args_len);
  // Serial.flush();
}
