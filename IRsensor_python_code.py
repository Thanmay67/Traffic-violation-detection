"""
Project: Automated Red-Light Violation Detection System
File: IRsensor_python_code.py
Description: Monitors the Arduino serial port for violation signals and
             commands an Android device via ADB to trigger the camera.
"""

import serial
import os
import time

# System Configurations
ARDUINO_PORT = 'COM6' 
BAUD_RATE = 9600
ADB_PATH = r"C:\Users\thanm\Downloads\platform-tools-latest-windows\platform-tools\adb.exe"

print("====================================================")
print("     AUTOMATED TRAFFIC ENFORCEMENT CAMERA ONLINE     ")
print("====================================================")
print(f"[SYSTEM]: Initializing connection on {ARDUINO_PORT}...")

try:
    # Open serial port connection with an explicit timeout configuration
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2)  # Hardware grace period allowing Arduino to reset cleanly
    print("[SYSTEM]: Connection established. Monitoring stop line...")
    print("----------------------------------------------------")
    
    while True:
        # Check if incoming data bytes are sitting in the buffer
        if ser.in_waiting > 0:
            # Read the incoming string line and decode it cleanly
            incoming_data = ser.readline().decode('utf-8').strip()
            
            if "VIOLATION_DETECTED" in incoming_data:
                print(f"\n[ALERT]: {time.strftime('%H:%M:%S')} - RED LIGHT RUNNER DETECTED!")
                print("-> Dispatching remote ADB shutter command to smartphone...")
                
                # Execute the native camera key event trigger
                os.system(f'"{ADB_PATH}" shell input keyevent KEYCODE_CAMERA')
                print("[SUCCESS]: Evidence photo captured.")
                
                # Stabilization cooldown to prevent accidental double-shutter triggers
                time.sleep(2.5)
                ser.reset_input_buffer()
                print("\n[SYSTEM]: Monitoring resumed. Watching stop line...")
                
except KeyboardInterrupt:
    print("\n[SYSTEM]: Manual shutdown request received. Closing camera bridge.")
except Exception as e:
    print(f"\n[CRITICAL ERROR]: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()