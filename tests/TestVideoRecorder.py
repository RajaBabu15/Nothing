from src.video_recorder.recorder import VideoRecorder

# Record for 5 seconds and save to a different directory
with VideoRecorder(filename="my_video.avi", duration=5, directory="my_recordings") as recorder:
    pass

# Or, if you want to use a custom stop callback:
def stop_on_loud_sound(video_frame, frame_counts, elapsed_time):
    # This is just an example. You'd need to implement actual loudness detection.
    return frame_counts > 100  # Stop after 100 frames

recorder = VideoRecorder(filename="loud_sound.avi", stop_callback=stop_on_loud_sound, directory="my_recordings")
recorder.start()
recorder.join()
