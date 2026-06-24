import serial
import os
import time
import subprocess

# --- CONFIGURATIONS ---
ARDUINO_PORT = 'COM6' 
BAUD_RATE = 9600
ADB_PATH = r"C:\Users\thanm\Downloads\platform-tools-latest-windows\platform-tools\adb.exe"
IMAGE_DIR = r"C:\Users\thanm\Desktop\IR sensor trafic violation detector"

print("====================================================")
print("     AUTOMATED TRAFFIC ENFORCEMENT CAMERA ONLINE     ")
print("====================================================")

try:
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2) # Wait for Arduino to reset
    print("[SYSTEM]: Tracking stop line on COM6...")
    
    while True:
        if ser.in_waiting > 0:
            incoming_data = ser.readline().decode('utf-8').strip()
            
            if "VIOLATION_DETECTED" in incoming_data:
                print(f"\n[ALERT]: {time.strftime('%H:%M:%S')} - RED LIGHT VIOLATION!")
                
                # 1. Snap the photo on the phone
                print("-> Snapping photo...")
                subprocess.run([ADB_PATH, "shell", "input", "keyevent", "KEYCODE_CAMERA"], shell=True)
                
                # Give the phone 3 seconds to fully save the photo
                time.sleep(3) 
                
                # 2. SMART PYTHON SORTING: Get file list directly from phone
                print("-> Reading phone gallery files...")
                cmd_list = f'"{ADB_PATH}" shell ls /sdcard/DCIM/Camera/'
                raw_files = subprocess.check_output(cmd_list, shell=True).decode('utf-8').splitlines()
                
                # Filter out anything that isn't a picture file (keeps .jpg, .jpeg, .png)
                img_files = [f.strip() for f in raw_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                if img_files:
                    # Android automatically names photos by timestamp (e.g., 20261114_...). 
                    # Sorting alphabetically gives us the absolute newest file at the end!
                    img_files.sort()
                    newest_filename = img_files[-1]
                    
                    print(f"-> Target acquired: {newest_filename}")
                    
                    # 3. Pull ONLY that single file
                    phone_path = f"/sdcard/DCIM/Camera/{newest_filename}"
                    subprocess.run([ADB_PATH, "pull", phone_path, IMAGE_DIR], shell=True)
                    
                    # 4. Rename it to latest_violation.jpg for the web dashboard
                    local_old_path = os.path.join(IMAGE_DIR, newest_filename)
                    local_new_path = os.path.join(IMAGE_DIR, "latest_violation.jpg")
                    
                    if os.path.exists(local_new_path):
                        os.remove(local_new_path)
                    os.rename(local_old_path, local_new_path)
                    
                    print("[SUCCESS]: Web dashboard storage updated.")
                else:
                    print("[WARNING]: No image files found on your phone camera roll.")
                
                time.sleep(1)
                ser.reset_input_buffer()
                print("\n[SYSTEM]: Monitoring resumed...")
                
except KeyboardInterrupt:
    print("\n[SYSTEM]: Closing camera bridge.")
except Exception as e:
    print(f"\n[ERROR]: {e}")