const byte SENSOR_PIN = 3; // Signal wire must be in Pin 3

void setup() {
  Serial.begin(9600);
  pinMode(SENSOR_PIN, INPUT_PULLUP); // Keeps the line stable
  Serial.println("STARTUP_COMPLETE");
}

void loop() {
  // If the sensor is blocked, its signal goes LOW (0)
  if (digitalRead(SENSOR_PIN) == LOW) {
    Serial.println("SNAP_PHOTO");
    delay(2000); // 2-second delay so it doesn't spam photos
  }
}