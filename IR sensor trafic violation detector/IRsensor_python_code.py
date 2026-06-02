import serial
import os
import time

arduino_port = 'COM6' 
baud_rate = 9600

print("--- Raw Byte Photo Gate Active ---")
print(f"Listening to {arduino_port}...")

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=0.1)
    time.sleep(2) # Wait for Arduino to reset
    print("System ready. Wave your hand!")
    
    while True:
        # Check if ANY raw bytes have arrived from the Arduino
        if ser.in_waiting > 0:
            raw_data = ser.read(ser.in_waiting)
            print(f"[Raw Data Detected!]: {raw_data}")
            
            print("-> Triggering phone shutter immediately...")
            os.system("adb shell input keyevent KEYCODE_CAMERA")
            
            # Prevent spamming commands
            time.sleep(2)
            ser.reset_input_buffer()
                
except KeyboardInterrupt:
    print("\nStopping script.")
except Exception as e:
    print(f"\n[ERROR]: {e}")