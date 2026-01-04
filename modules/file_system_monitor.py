import time
import os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from modules.event_classifier import EventClassifier
from modules.sensitive_file_manager import SensitiveFileClassifier
from modules.integrity_checker import IntegrityChecker
from modules.authorization_engine import PolicyEngine
from modules.alert_manager import AlertManager
from modules.logging_engine import log_event

class SecurityMonitorHandler(FileSystemEventHandler):
    """
    Handles file system events and triggers security logic.
    """
    
    def _process_file_event(self, event_path, event_type, dest_path=None):
        # Ignore temporary files or standard directory noise
        if event_path.endswith('.tmp') or '~' in event_path:
            return

        # 1. Classification
        is_sensitive, classification_reason = SensitiveFileClassifier.classify_file(event_path)
        
        # 2. Integrity Check (Pre-computation if needed, though for single events we usually check current state)
        file_hash = IntegrityChecker.calculate_sha256(event_path) if os.path.exists(event_path) and not os.path.isdir(event_path) else "N/A"
        
        details = {
            "path": event_path,
            "is_sensitive": is_sensitive,
            "classification": classification_reason,
            "hash": file_hash
        }
        
        if dest_path:
            details["destination"] = dest_path
            
            # Policy Check for Moves/Copies
            status, msg, severity = PolicyEngine.check_movement_policy(event_path, dest_path, is_sensitive)
            if status != "ALLOWED":
                AlertManager.trigger_alert(severity, msg, details)
            else:
                log_event(event_type, details)
                
        else:
            # Policy/Alerting for other events
            if event_type == "FILE_MODIFIED" and is_sensitive:
                # Alert on modification of sensitive files
                 AlertManager.trigger_alert("LOW", "Sensitive file modified", details)
            elif event_type == "FILE_DELETED" and is_sensitive:
                 AlertManager.trigger_alert("MEDIUM", "Sensitive file deleted", details)
            else:
                log_event(event_type, details)

    def on_created(self, event):
        if event.is_directory: return
        event_type = EventClassifier.classify_event(event)
        self._process_file_event(event.src_path, event_type)

    def on_deleted(self, event):
        if event.is_directory: return
        event_type = EventClassifier.classify_event(event)
        # Note: Cannot compute hash of deleted file
        log_event(event_type, {"path": event.src_path, "status": "DELETED"})

    def on_modified(self, event):
        if event.is_directory: return
        event_type = EventClassifier.classify_event(event)
        self._process_file_event(event.src_path, event_type)

    def on_moved(self, event):
        if event.is_directory: return
        event_type = EventClassifier.classify_event(event)
        self._process_file_event(event.src_path, event_type, dest_path=event.dest_path)

class FileSystemMonitor:
    def __init__(self, path):
        self.path = path
        self.observer = Observer()
        self.handler = SecurityMonitorHandler()

    def start(self):
        print(f"[*] Starting File System Monitor on: {self.path}")
        self.observer.schedule(self.handler, self.path, recursive=True)
        self.observer.start()

    def stop(self):
        print("[*] Stopping File System Monitor...")
        self.observer.stop()
        self.observer.join()
