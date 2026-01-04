import os
import time
import shutil

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONITOR_ZONE = os.path.join(BASE_DIR, 'data', 'monitoring_zone')
SECURE_ZONE = os.path.join(MONITOR_ZONE, 'secure_docs')
USB_ZONE = os.path.join(MONITOR_ZONE, 'external_usb')

# Target file provided by user
USER_FILE_NAME = 'LuminaCore_FY26_Market_Analysis.docx'
USER_FILE_PATH = os.path.join(SECURE_ZONE, USER_FILE_NAME)

def setup():
    print("[*] Setting up simulation environment...")
    os.makedirs(SECURE_ZONE, exist_ok=True)
    os.makedirs(USB_ZONE, exist_ok=True)

def simulate_activity():
    print(f"\n--- Starting Advanced Simulation ---")
    print(f"Targeting sensitive file: {USER_FILE_NAME}")
    
    # 1. Check if user file exists, else create a dummy one
    if not os.path.exists(USER_FILE_PATH):
        print(f"[!] User file not found. Creating dummy {USER_FILE_NAME}...")
        with open(USER_FILE_PATH, 'w') as f:
            f.write("CONFIDENTIAL MARKET DATA - TOP SECRET")
    else:
        print(f"[+] Found existing sensitive file: {USER_FILE_PATH}")
    
    time.sleep(2)

    # 2. Simulate User Modifying the File (Integrity Check)
    print(f"\n[1] ACTION: Modifying {USER_FILE_NAME} (Simulating work in progress)...")
    try:
        with open(USER_FILE_PATH, 'a') as f:
            f.write("\n[UPDATE] Q4 Projections added.")
        print("--> File modified. Monitor should log 'FILE_MODIFIED' and potentially ALERT if strict.")
    except Exception as e:
        print(f"[!] Error modifying file: {e}")
    
    time.sleep(3)
    
    # 3. Simulate Unauthorized Exfiltration (Copy to USB)
    print(f"\n[2] ACTION: ATTACK! Copying {USER_FILE_NAME} to External USB...")
    dst_path = os.path.join(USB_ZONE, USER_FILE_NAME)
    
    try:
        shutil.copy2(USER_FILE_PATH, dst_path)
        print(f"--> File copied to {dst_path}")
        print("--> EXPECTED: CRITICAL ALERT 'Sensitive file moved to external device'")
    except Exception as e:
        print(f"[!] Error copying file: {e}")

    time.sleep(2)
    
    # 4. Cleanup (Optional - uncomment if you want to reset)
    # if os.path.exists(dst_path):
    #     os.remove(dst_path)
    #     print("\n[!] Cleanup: Removed file from USB zone.")

    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    setup()
    simulate_activity()
