# tests/TestAudioRecorder.py

import unittest
from src.audio_recorder.recorder import AudioRecorder

class TestAudioRecorder(unittest.TestCase):

    def test_audio_recording_basic(self):
        """Test basic audio recording functionality."""
        try:
            with AudioRecorder(filename="my_audio.wav", duration=5, directory="test_recordings") as recorder:
                pass
            self.assertTrue(True, "Audio recording completed successfully.")
        except Exception as e:
            self.fail(f"Audio recording failed with exception: {e}")

    def test_audio_recording_with_stop_callback(self):
        """Test audio recording with a custom stop callback based on loudness."""

        def stop_on_loud_sound(data, frames_per_buffer, elapsed_time, audio_frames):
            # Example logic for loudness detection
            return max(abs(int.from_bytes(data, byteorder='little', signed=True)) for _ in range(frames_per_buffer)) > 1000

        try:
            recorder = AudioRecorder(filename="loud_sound.wav", stop_callback=stop_on_loud_sound, directory="test_recordings")
            recorder.start()
            recorder.join()  # Wait for the recording to finish
            self.assertTrue(True, "Audio recording with stop callback completed successfully.")
        except Exception as e:
            self.fail(f"Audio recording with stop callback failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
