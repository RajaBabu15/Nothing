# tests/TestVideoRecorder.py

import unittest
from src.video_recorder.recorder import VideoRecorder

class TestVideoRecorder(unittest.TestCase):

    def test_video_recording_basic(self):
        """Test basic video recording functionality."""
        try:
            with VideoRecorder(filename="my_video.avi", duration=5, directory="test_recordings") as recorder:
                pass
            self.assertTrue(True, "Video recording completed successfully.")
        except Exception as e:
            self.fail(f"Video recording failed with exception: {e}")

    def test_video_recording_with_stop_callback(self):
        """Test video recording with a custom stop callback for motion detection."""

        def stop_on_motion(video_frame, frame_counts, elapsed_time):
            # Example logic to detect motion or stop after 100 frames
            # For now, we simply stop after a certain frame count
            return frame_counts > 100

        try:
            recorder = VideoRecorder(filename="motion_detected.avi", stop_callback=stop_on_motion, directory="test_recordings")
            recorder.start()
            recorder.join()  # Wait for the recording to finish
            self.assertTrue(True, "Video recording with stop callback completed successfully.")
        except Exception as e:
            self.fail(f"Video recording with stop callback failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
