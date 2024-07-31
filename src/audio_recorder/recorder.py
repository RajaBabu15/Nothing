import pyaudio
import wave
import threading
import time
import os
from common.file_management import get_unique_filename, create_output_directory
from common.config import AUDIO_SETTINGS, OUTPUT_DIRECTORIES
from common.exceptions import AudioRecorderError

class AudioRecorder:
    def __init__(self, filename="temp_audio.wav", directory=None, frame_callback=None, duration=10, stop_callback=None):
        self.open = False
        self.rate = AUDIO_SETTINGS['rate']
        self.frames_per_buffer = AUDIO_SETTINGS['frames_per_buffer']
        self.channels = AUDIO_SETTINGS['channels']
        self.format = pyaudio.paInt16  # Convert format string to actual PyAudio format
        self.directory = directory or OUTPUT_DIRECTORIES['audio']
        
        create_output_directory(self.directory)
        self.filename = get_unique_filename(filename, self.directory)
        self.full_path = os.path.join(self.directory, self.filename)
        self.frame_callback = frame_callback
        self.duration = duration
        self.stop_callback = stop_callback
        self.audio = pyaudio.PyAudio()
        self.audio_stream = None
        self.audio_frames = []
        self.thread = None

    def record(self):
        try:
            self.audio_stream = self.audio.open(format=self.format,
                                                channels=self.channels,
                                                rate=self.rate,
                                                input=True,
                                                frames_per_buffer=self.frames_per_buffer)
            self.audio_stream.start_stream()
            self.open = True
            start_time = time.time()

            print("Audio Recording Started")
            while self.open:
                data = self.audio_stream.read(self.frames_per_buffer)
                self.audio_frames.append(data)
                elapsed_time = time.time() - start_time
                if self.frame_callback:
                    self.frame_callback(data, self.frames_per_buffer, elapsed_time, self.audio_frames)
                if self.stop_callback and self.stop_callback(data, self.frames_per_buffer, elapsed_time, self.audio_frames):
                    break
                if not self.stop_callback and elapsed_time >= self.duration:
                    break

        except Exception as e:
            raise AudioRecorderError(f"An error occurred during audio recording: {e}")

        finally:
            self.stop()

    def stop(self):
        if self.open:
            self.open = False
            if self.audio_stream:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            self.audio.terminate()

            print(f"Audio Recording complete! Saving to: {self.full_path}")

            with wave.open(self.full_path, 'wb') as waveFile:
                waveFile.setnchannels(self.channels)
                waveFile.setsampwidth(self.audio.get_sample_size(self.format))
                waveFile.setframerate(self.rate)
                waveFile.writeframes(b''.join(self.audio_frames))
            print("Audio Recording saved successfully!")

    def start(self):
        self.thread = threading.Thread(target=self.record)
        self.thread.start()
        self.thread.join()  

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.thread and self.thread.is_alive():
            self.stop()
            self.thread.join()
