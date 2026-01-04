from watchdog.events import FileSystemEvent

class EventClassifier:
    """
    Classifies raw watchdog events into business logic events.
    """
    
    @staticmethod
    def classify_event(event: FileSystemEvent):
        if event.is_directory:
            return "DIRECTORY_EVENT"
            
        event_type = event.event_type
        
        mapping = {
            'created': 'FILE_CREATED',
            'deleted': 'FILE_DELETED',
            'modified': 'FILE_MODIFIED',
            'moved': 'FILE_MOVED'
        }
        
        return mapping.get(event_type, "UNKNOWN_EVENT")
