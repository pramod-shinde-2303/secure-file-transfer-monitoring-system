import time
import sys
import os
from config import settings
from modules.logging_engine import setup_logger, log_event
from modules.file_system_monitor import FileSystemMonitor
from modules.report_generator import ReportGenerator

def main():
    # 1. Setup
    print("--------------------------------------------------")
    print("   SECURE FILE TRANSFER MONITORING SYSTEM")
    print("--------------------------------------------------")
    
    logger = setup_logger()
    log_event("SYSTEM", {"status": "STARTUP", "scope": settings.MONITOR_PATH})
    
    print(f"[*] Configuration Loaded.")
    print(f"[*] Monitoring Zone: {settings.MONITOR_PATH}")
    print(f"[*] Log File: {settings.LOG_FILE}")
    print("[*] Press Ctrl+C to stop monitoring and generate report.")
    print("--------------------------------------------------")

    # 2. Start Monitor
    monitor = FileSystemMonitor(settings.MONITOR_PATH)
    monitor.start()
    
    # 3. Keep Alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Stopping system by user request...")
        monitor.stop()
        
    # 4. Generate Report
    print("[*] Generating Final Audit Report...")
    report_path = ReportGenerator.generate_report()
    
    log_event("SYSTEM", {"status": "SHUTDOWN", "report": report_path})
    print(f"[*] Report generated at: {report_path}")
    print("[*] System Shutdown Complete.")

if __name__ == "__main__":
    main()
