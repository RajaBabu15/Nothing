from src.audio_recorder.recorder import AudioRecorder

# Record for 5 seconds
with AudioRecorder(filename="my_audio.wav", duration=5) as recorder:
    pass


# Or, if you want to use a custom stop callback:
def stop_on_loud_sound(data, frames_per_buffer, elapsed_time, audio_frames):
    # This is just an example. You'd need to implement actual loudness detection.
    return max(abs(int.from_bytes(data, byteorder='little', signed=True)) for _ in range(frames_per_buffer)) > 1000

recorder = AudioRecorder(filename="loud_sound.wav", stop_callback=stop_on_loud_sound)
recorder.start()