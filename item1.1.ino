void iniciarPiano() {
  for (int i = 0; i < 3; i++) {
    pinMode(leds[i], OUTPUT);
    pinMode(botones[i], INPUT_PULLUP);
  }
  pinMode(buzzer, OUTPUT);
}

void ejecutarPiano() {
  for (int i = 0; i < 3; i++) {
    if (digitalRead(botones[i]) == LOW) {
      digitalWrite(leds[i], HIGH);

      int nota = bancos[banco][i];
      tone(buzzer, nota, 200);  // tono
      analogWrite(buzzer, volumen); // volumen PWM (solo si buzzer lo soporta)

      Serial.print("Botón ");
      Serial.print(i);
      Serial.print(" presionado. Nota: ");
      Serial.println(nota);
      delay(300);
      digitalWrite(leds[i], LOW);
    }
  }
}