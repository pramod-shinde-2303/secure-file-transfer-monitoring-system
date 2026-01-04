import os
from config import settings

class SensitiveFileClassifier:
    """
    Classifies files based on sensitivity rules defined in settings.
    """
    
    @staticmethod
    def is_sensitive_extension(filename):
        _, ext = os.path.splitext(filename)
        return ext.lower() in settings.SENSITIVE_EXTENSIONS

    @staticmethod
    def is_sensitive_keyword(filename):
        name = os.path.basename(filename).lower()
        return any(keyword in name for keyword in settings.SENSITIVE_KEYWORDS)

    @staticmethod
    def is_sensitive_path(path):
        # Check if the file resides in a known secure zone (optional helper)
        return settings.SECURE_ZONE in os.path.abspath(path)

    @classmethod
    def classify_file(cls, file_path):
        """
        Determines if a file is sensitive.
        Returns: (is_sensitive: bool, reason: str)
        """
        if cls.is_sensitive_extension(file_path):
            return True, "Restricted Extension"
        
        if cls.is_sensitive_keyword(file_path):
            return True, "Sensitive Keyword in Filename"
            
        return False, "Non-Sensitive"
