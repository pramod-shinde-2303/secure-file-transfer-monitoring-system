import os
from config import settings

class PolicyEngine:
    """
    Analyzes file events to detect policy violations.
    """
    
    @staticmethod
    def check_movement_policy(src_path, dst_path, is_sensitive):
        """
        Evaluates if a file movement is authorized.
        """
        dst_folder = os.path.dirname(os.path.abspath(dst_path))
        
        # Rule 1: Sensitive file moved to unauthorized location (e.g., USB)
        if is_sensitive:
            if settings.EXTERNAL_DEVICE_PATH in dst_folder:
                return "VIOLATION", "Sensitive file moved to external device", "HIGH"
            
            # If moved out of secure zone to general monitoring zone
            if settings.SECURE_ZONE in os.path.dirname(os.path.abspath(src_path)) and \
               settings.SECURE_ZONE not in dst_folder:
                return "WARNING", "Sensitive file moved out of secure zone", "MEDIUM"
                
        # Rule 2: Any movement to external device
        if settings.EXTERNAL_DEVICE_PATH in dst_folder:
             return "INFO", "File moved to external device", "LOW"

        return "ALLOWED", "Authorized movement", "INFO"

    @staticmethod
    def check_integrity_violation(old_hash, new_hash):
        if old_hash and new_hash and old_hash != new_hash:
            return True
        return False
