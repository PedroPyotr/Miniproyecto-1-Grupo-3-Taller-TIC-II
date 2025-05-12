int puntaje = 0;
int racha = 0;

void iniciarJuego() {
  for (int i = 0; i < 3; i++) {
    pinMode(leds[i], OUTPUT);
    pinMode(botones[i], INPUT_PULLUP);
  }
  pinMode(buzzer, OUTPUT);
}

void mostrarMenu() {
  Serial.println("\n==== GUITAR HERO ====");
  Serial.println("Selecciona dificultad:");
  Serial.println("D0 - Facil");
  Serial.println("D1 - Medio");
  Serial.println("D2 - Dificil");
  Serial.println("Selecciona canción:");
  Serial.println("C0 - Canción 1");
  Serial.println("C1 - Canción 2");
  Serial.println("C2 - Canción 3");
  Serial.println("Escribe 'inicio' para comenzar el juego.");
}

void jugarGuitarHero() {
  puntaje = 0;
  racha = 0;

  for (int i = 0; i < largoCancion; i++) {
    int nota = canciones[cancionSeleccionada][i];
    digitalWrite(leds[nota], HIGH);
    tone(buzzer, 262 + nota * 100);
    unsigned long start = millis();
    bool acierto = false;

    while (millis() - start < velocidades[dificultad]) {
      if (digitalRead(botones[nota]) == LOW) {
        acierto = true;
        break;
      } else {
        // Si presiona otro botón, se considera fallo
        for (int j = 0; j < 3; j++) {
          if (j != nota && digitalRead(botones[j]) == LOW) {
            acierto = false;
            goto salir;
          }
        }
      }
    }

    salir:
    digitalWrite(leds[nota], LOW);
    noTone(buzzer);

    if (acierto) {
      racha++;
      int multiplicador = 1;
      if (racha >= 20) multiplicador = 16;
      else if (racha >= 15) multiplicador = 8;
      else if (racha >= 10) multiplicador = 4;
      else if (racha >= 5) multiplicador = 2;

      puntaje += 10 * multiplicador;
      Serial.print("¡Bien! Puntaje: ");
      Serial.println(puntaje);
    } else {
      racha = 0;
      puntaje -= 10;
      Serial.print("¡Fallaste! Puntaje: ");
      Serial.println(puntaje);
      if (puntaje <= 0) {
        Serial.println("GAME OVER");
        tone(buzzer, 200, 1000);
        delay(1000);
        noTone(buzzer);
        return;
      }
    }

    delay(200); // Pausa entre notas
  }

  if (puntaje > 0) {
    Serial.print("¡Ganaste! Puntaje final: ");
    Serial.println(puntaje);
    tonoVictoria();
  } else {
    Serial.print("Puntaje final: ");
    Serial.println(puntaje);
  }
}

void tonoVictoria() {
  tone(buzzer, 523, 200); delay(250);
  tone(buzzer, 659, 200); delay(250);
  tone(buzzer, 784, 400); delay(450);
  noTone(buzzer);
}