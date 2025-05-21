// Pines para el LED RGB (cátodo común)
const int PIN_ROJO = 11;
const int PIN_VERDE = 10;
const int PIN_AZUL = 9;

// Pin para el botón de reinicio
const int PIN_BOTON = 13;

// Variable para almacenar la cantidad de células vivas
int celulasVivas = 0;

void setup() {
  // Inicializar la comunicación serial
  Serial.begin(9600);

  // Configurar los pines del LED como salidas
  pinMode(PIN_ROJO, OUTPUT);
  pinMode(PIN_VERDE, OUTPUT);
  pinMode(PIN_AZUL, OUTPUT);

  // Configurar el pin del botón como entrada con resistencia pull-up interna
  pinMode(PIN_BOTON, INPUT_PULLUP);
}

void loop() {
  // Verificar si hay datos disponibles en el puerto serie
  if (Serial.available() > 1) {
    int cantidad = Serial.parseInt();
    actualizarColorLED(cantidad);
  }

  // Verificar si el botón ha sido presionado
  if (digitalRead(PIN_BOTON) == LOW) {
    Serial.println("REINICIAR");
    delay(500); // Esperar para evitar múltiples lecturas (debounce)
  }
}

// Función para actualizar el color del LED según la cantidad de células vivas
void actualizarColorLED(int cantidad) {
  if (cantidad > 4000) {
    // Amarillo
    analogWrite(PIN_ROJO, 255);
    analogWrite(PIN_VERDE, 150);
    analogWrite(PIN_AZUL, 0);
  } else if (cantidad >= 2000) {
    // Verde
    analogWrite(PIN_ROJO, 0);
    analogWrite(PIN_VERDE, 255);
    analogWrite(PIN_AZUL, 0);
  } else {
    // Rojo
    analogWrite(PIN_ROJO, 255);
    analogWrite(PIN_VERDE, 0);
    analogWrite(PIN_AZUL, 0);
  }
}
