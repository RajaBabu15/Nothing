# Define global configuration settings

AUDIO_SETTINGS = {
    "rate": 44100,
    "frames_per_buffer": 1024,
    "channels": 2,
    "format": 'paInt16',  # Change as necessary
}

VIDEO_SETTINGS = {
    "device_index": 0,
    "fps": 30,
    "frame_size": (640, 480),
    "codec": "MJPG",
}

OUTPUT_DIRECTORIES = {
    "audio": "recordings/audio",
    "video": "recordings/video",
}
