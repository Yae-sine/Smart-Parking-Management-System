// #include <ESP32Servo.h>
// #include <LiquidCrystal_I2C.h>

#define trig1 18
#define echo1 19
#define motor1Pin 5  

#define trig2 2
#define echo2 23
#define motor2Pin 4 

LiquidCrystal_I2C lcd(0x27, 16, 2);  

Servo servoEntree;
Servo servoSortie;

bool parkingPlein = false;

void setup() {
  Serial.begin(115200);

  Wire.begin(21, 22);  // SDA sur 21, SCL sur 22 (par défaut pour ESP32)
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("AI Parking");

  pinMode(trig1, OUTPUT);
  pinMode(echo1, INPUT);
  pinMode(trig2, OUTPUT);
  pinMode(echo2, INPUT);

  // Attacher les servos à différents canaux PWM
  servoEntree.setPeriodHertz(50);
  servoEntree.attach(motor1Pin, 500, 2400);

  servoSortie.setPeriodHertz(50);
  servoSortie.attach(motor2Pin, 500, 2400);

  // Position initiale des servos
  servoEntree.write(0);
  servoSortie.write(0);
}

long getDistance(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  return pulseIn(echo, HIGH) * 0.034 / 2;
}

void loop() {
  long distanceEntree = getDistance(trig1, echo1);
  long distanceSortie = getDistance(trig2, echo2);

  // Test manuel : simule l’état de plein ou pas
  parkingPlein = false;  // Change ça pour tester

  // Gestion entrée
  if (distanceEntree < 7) {
    if (!parkingPlein) {
      servoEntree.write(90);
      lcd.setCursor(0, 1);
      lcd.print("AI Parking     ");
    } else {
      lcd.setCursor(0, 1);
      lcd.print("Parking plein  ");
    }
  } else {
    if (!parkingPlein) servoEntree.write(0);
  }

  // Gestion sortie
  if (distanceSortie < 7) {
    servoSortie.write(90);
    lcd.setCursor(0, 1);
    lcd.print("AI Parking     ");
  } else {
    servoSortie.write(0);
  }
  delay(300);
}