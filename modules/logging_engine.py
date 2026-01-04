import logging
import json
import os
from datetime import datetime
from config import settings

class JsonFormatter(logging.Formatter):
    """
    Formatter to output logs in JSON format.
    """
    def format(self, record):
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "event": record.msg,
            "module": record.module
        }
        # Add any extra attributes passed in the extra dict
        if hasattr(record, 'extra_data'):
            log_entry.update(record.extra_data)
        
        return json.dumps(log_entry)

def setup_logger():
    """
    Sets up the application logger.
    """
    logger = logging.getLogger('SecureFileMonitor')
    logger.setLevel(logging.INFO)
    
    # File Handler (JSON)
    file_handler = logging.FileHandler(settings.LOG_FILE)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JsonFormatter())
    
    # Console Handler (Human Readable)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Prevent adding handlers multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

def log_event(event_type, details, severity="INFO"):
    """
    Helper function to log structured events.
    """
    logger = logging.getLogger('SecureFileMonitor')
    extra = {"extra_data": {"type": event_type, **details}}
    
    if severity == "HIGH":
        logger.critical(f"{event_type}: {details}", extra=extra)
    elif severity == "MEDIUM":
        logger.warning(f"{event_type}: {details}", extra=extra)
    elif severity == "LOW":
        logger.info(f"{event_type}: {details}", extra=extra)
    else:
        logger.debug(f"{event_type}: {details}", extra=extra)
