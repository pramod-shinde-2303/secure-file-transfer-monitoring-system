from modules.logging_engine import log_event

class AlertManager:
    """
    Manages the generation and distribution of alerts.
    """
    
    @staticmethod
    def trigger_alert(severity, message, details=None):
        """
        Triggers an alert based on severity.
        """
        if details is None:
            details = {}
            
        print_prefix = ""
        if severity == "HIGH":
            print_prefix = "!!! CRITICAL SECURITY ALERT !!!"
        elif severity == "MEDIUM":
            print_prefix = "! WARNING !"
        elif severity == "LOW":
            print_prefix = "* NOTICE *"
            
        # Console output for immediate visibility
        if severity in ["HIGH", "MEDIUM"]:
            print(f"\n{print_prefix} {message}")
            if details:
                print(f"Details: {details}\n")
        
        # Log the alert
        log_event("ALERT", {
            "severity": severity,
            "message": message,
            "details": details
        }, severity=severity)
