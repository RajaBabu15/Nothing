import os
from AudioRecorder import AudioRecorder

class AudioRecorderTester:
    def __init__(self, filename="Test_audio"):
        self.filename = filename + ".wav"
        self._remove_existing_file(self.filename)
        self.recorder = None

    def _remove_existing_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)

    def default_audio_callback(self, data, frames_per_buffer, elapsed_time, audio_frames):
        pass

    def custom_audio_callback(self, data, frames_per_buffer, elapsed_time, audio_frames):
        pass

    def stop_callback(self, data, frames_per_buffer, elapsed_time, audio_frames):
        return elapsed_time >= 5

    def start_test(self, use_custom_callback=False):
        audio_callback = self.custom_audio_callback if use_custom_callback else self.default_audio_callback
        self.recorder = AudioRecorder(filename=self.filename, frame_callback=audio_callback)
        
        self.recorder.start(stop_callback=self.stop_callback)
        self.recorder.join()

if __name__ == "__main__":
    tester = AudioRecorderTester()
    tester.start_test(use_custom_callback=False)