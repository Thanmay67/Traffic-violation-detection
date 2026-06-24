/*
  Project: Automated Red-Light Violation Detection System
  File: IRsensor_arduino_code.cpp
  Description: Manages a 3-LED traffic cycle state machine and monitors an
               IR sensor pin for lane violations strictly during the RED phase.
*/

// Hardware Pin Definitions
const byte SENSOR_PIN = 3;   // IR Proximity Sensor Out
const byte GREEN_LED  = 10;  // Intersection Green Light
const byte YELLOW_LED = 11;  // Intersection Yellow Light
const byte RED_LED    = 12;  // Intersection Red Light / Strobe Flash

// Timing Phase Configurations (Milliseconds)
const unsigned long GREEN_DURATION  = 5000; // 5 seconds
const unsigned long YELLOW_DURATION = 2000; // 2 seconds
const unsigned long RED_DURATION    = 5000; // 5 seconds
const unsigned long COOLDOWN_PERIOD = 2500; // Time window before another photo can snap

// State Machine Variable Trackers
unsigned long lightTimer = 0;
int lightState = 0; // 0 = Green, 1 = Yellow, 2 = Red

void setup() {
  Serial.begin(9600);
  
  // Initialize digital inputs and outputs
  pinMode(SENSOR_PIN, INPUT_PULLUP);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  
  lightTimer = millis(); // Benchmark system start time
}

void loop() {
  unsigned long currentTime = millis();

  // 1. Core State Machine: Managing the Intersections Traffic Signal Cycles
  if (lightState == 0 && (currentTime - lightTimer > GREEN_DURATION)) { 
    lightState = 1; // Transition Green -> Yellow
    lightTimer = currentTime;
  } 
  else if (lightState == 1 && (currentTime - lightTimer > YELLOW_DURATION)) { 
    lightState = 2; // Transition Yellow -> Red
    lightTimer = currentTime;
  } 
  else if (lightState == 2 && (currentTime - lightTimer > RED_DURATION)) { 
    lightState = 0; // Transition Red -> Reset to Green
    lightTimer = currentTime;
  }

  // 2. Physical Output Driver Logic
  digitalWrite(GREEN_LED,  lightState == 0 ? HIGH : LOW);
  digitalWrite(YELLOW_LED, lightState == 1 ? HIGH : LOW);
  digitalWrite(RED_LED,    lightState == 2 ? HIGH : LOW);

  // 3. Conditional Enforcement Logic (Exclusively operational during RED phase)
  if (lightState == 2) {
    // Check if a vehicle passes the stop-line sensor (Low signal indicates beam-break)
    if (digitalRead(SENSOR_PIN) == LOW) {
      Serial.println("VIOLATION_DETECTED"); // Dispatch alert byte flag to Python
      
      // Visual Feedback Loop: Rapidly pulse the red LED to emulate camera flash units
      for (int i = 0; i < 3; i++) {
        digitalWrite(RED_LED, LOW);  delay(80);
        digitalWrite(RED_LED, HIGH); delay(80);
      }
      
      delay(COOLDOWN_PERIOD); // Hardware tracking lock to ensure a single capture per event
    }
  }
}