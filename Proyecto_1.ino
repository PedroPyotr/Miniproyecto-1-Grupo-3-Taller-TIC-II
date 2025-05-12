#include "pines.h"

int modo = 0; // 0 = piano, 1 = guitar hero
bool listoParaJugar = false;

void setup() {
  Serial.begin(9600);
  iniciarPiano();
  iniciarJuego();
  Serial.println("Escribe 'piano' o 'juego' para cambiar de modo.");
}

void loop() {
  verificarSerialModo();

  if (modo == 0) {
    ejecutarPiano();
  } else if (modo == 1 && listoParaJugar) {
    jugarGuitarHero();
    modo = 0;
    listoParaJugar = false;
    Serial.println("Juego terminado. Volviendo a modo piano.");
  }
}

void verificarSerialModo() {
  if (Serial.available()) {
    String entrada = Serial.readStringUntil('\n');
    entrada.trim();

    if (entrada.equalsIgnoreCase("piano")) {
      modo = 0;
      Serial.println("Modo cambiado a Piano.");
    } else if (entrada.equalsIgnoreCase("juego")) {
      modo = 1;
      mostrarMenu();
    } else if (entrada.startsWith("D")) {
      dificultad = entrada.substring(1).toInt();
      Serial.print("Dificultad seleccionada: ");
      Serial.println(dificultad);
    } else if (entrada.startsWith("C")) {
      cancionSeleccionada = entrada.substring(1).toInt();
      Serial.print("Canción seleccionada: ");
      Serial.println(cancionSeleccionada);
    } else if (entrada.startsWith("V")) {
      volumen = entrada.substring(1).toInt();
      volumen = constrain(volumen, 0, 255);
      Serial.print("Volumen actualizado a: ");
      Serial.println(volumen);
    } else if (entrada.startsWith("T")) {
      int t = entrada.substring(1).toInt();
      if (t == 0 && banco > 0) banco--;
      else if (t == 1 && banco < 2) banco++;
      Serial.print("Banco de tonos: ");
      Serial.println(banco);
    } else if (entrada.equalsIgnoreCase("inicio")) {
      listoParaJugar = true;
      Serial.println("¡Comenzando juego!");
    }
  }
}
