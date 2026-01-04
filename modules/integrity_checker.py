import hashlib
import os

class IntegrityChecker:
    """
    Computes cryptographic hashes of files to verify integrity.
    """
    
    @staticmethod
    def calculate_sha256(file_path):
        """
        Reads file and returns SHA256 hash.
        Handles permission errors or file lock issues gracefully.
        """
        if not os.path.exists(file_path):
            return None
            
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                # Read in chunks to handle large files
                for byte_block in iter(lambda: f.read(65536), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except (PermissionError, OSError):
            return "ACCESS_DENIED_OR_BUSY"
        except Exception as e:
            return f"ERROR_COMPUTING_HASH: {str(e)}"
