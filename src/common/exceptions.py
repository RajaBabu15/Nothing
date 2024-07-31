class RecorderError(Exception):
    """Base class for recorder-related exceptions."""
    pass

class AudioRecorderError(RecorderError):
    """Exception raised for errors in the Audio Recorder."""
    pass

class VideoRecorderError(RecorderError):
    """Exception raised for errors in the Video Recorder."""
    pass
