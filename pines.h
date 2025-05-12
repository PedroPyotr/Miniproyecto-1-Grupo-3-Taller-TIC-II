// Pines
const int buzzer = 13;
const int leds[3] = {12, 11, 10};
const int botones[3] = {7, 6, 5};

// Parámetros de tono y volumen
int volumen = 255;  // PWM para buzzer (solo útil en buzzer pasivo o conectado a pin PWM)
int banco = 0;

// Notas por banco
int bancos[3][3] = {
  {262, 294, 330}, // C D E
  {330, 392, 440}, // E G A
  {440, 494, 523}  // A B C5
};

// Variables globales
int dificultad = 0;
int cancionSeleccionada = 0;

// Rango de tiempo por dificultad
int velocidades[] = {1000, 700, 400};

// Canciones (índices LED/nota)
const int canciones[3][6] = {
  {0, 1, 2, 1, 0, 2}, // Canción 0
  {2, 2, 1, 0, 1, 2}, // Canción 1
  {1, 0, 1, 2, 2, 0}  // Canción 2
};
const int largoCancion = 6;