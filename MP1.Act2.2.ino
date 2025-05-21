// LED RGB pins (cathode common)
const int PIN_R = 6;
const int PIN_G = 5;
const int PIN_B = 3;
// Buttons for events and reset
const int BTN1 = 9;
const int BTN2 = 10;
const int BTN3 = 11;
const int BTN4 = 12;
const int BTN_RST = 2;

void setup() {
  Serial.begin(9600);
  pinMode(PIN_R, OUTPUT);
  pinMode(PIN_G, OUTPUT);
  pinMode(PIN_B, OUTPUT);
  pinMode(BTN1, INPUT_PULLUP);
  pinMode(BTN2, INPUT_PULLUP);
  pinMode(BTN3, INPUT_PULLUP);
  pinMode(BTN4, INPUT_PULLUP);
  pinMode(BTN_RST, INPUT_PULLUP);
}

void loop() {
  if (Serial.available()) {
    int v = Serial.parseInt();
    if (v) {
      if (v > 7000) {
        analogWrite(PIN_R, 255); analogWrite(PIN_G, 0);   analogWrite(PIN_B, 0);
      } else if (v >= 3000) {
        analogWrite(PIN_R, 255); analogWrite(PIN_G, 255); analogWrite(PIN_B, 0);
      } else {
        analogWrite(PIN_R, 0);   analogWrite(PIN_G, 255); analogWrite(PIN_B, 0);
      }
    }
  }
  if (digitalRead(BTN1) == LOW) { Serial.println("a-1"); delay(200); }
  if (digitalRead(BTN2) == LOW) { Serial.println("a-2"); delay(200); }
  if (digitalRead(BTN3) == LOW) { Serial.println("a-3"); delay(200); }
  if (digitalRead(BTN4) == LOW) { Serial.println("a-4"); delay(200); }
  if (digitalRead(BTN_RST) == LOW) { Serial.println("r");   delay(200); }
}
