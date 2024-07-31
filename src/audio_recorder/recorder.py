import pyaudio
import wave
import threading
import time
import os
from .utils import get_unique_filename

class AudioRecorder:
    def __init__(self, rate=44100, frames_per_buffer=1024, channels=2, format=pyaudio.paInt16, 
                 filename="temp_audio.wav", directory="recordings", frame_callback=None, duration=10, stop_callback=None):
        self.open = False
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.channels = channels
        self.format = format
        self.directory = directory
        self.filename = get_unique_filename(filename)
        self.full_path = os.path.join(self.directory, self.filename)
        self.frame_callback = frame_callback
        self.duration = duration
        self.stop_callback = stop_callback
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.audio_frames = []
        self.start_time = time.time()
        self.thread = None

        # Ensure the directory exists
        os.makedirs(self.directory, exist_ok=True)

    def record(self):
        try:
            self.stream = self.audio.open(format=self.format,
                                          channels=self.channels,
                                          rate=self.rate,
                                          input=True,
                                          frames_per_buffer=self.frames_per_buffer)
            self.stream.start_stream()
            self.open = True
            start_time = time.time()
            
            if self.open:
                print("Recording...")
                self.audio_frames.clear()

            while self.open:
                data = self.stream.read(self.frames_per_buffer)
                self.audio_frames.append(data)

                elapsed_time = time.time() - start_time

                if self.frame_callback:
                    self.frame_callback(data, self.frames_per_buffer, elapsed_time, self.audio_frames)

                if self.stop_callback and self.stop_callback(data, self.frames_per_buffer, elapsed_time, self.audio_frames):
                    break

                if not self.stop_callback and elapsed_time >= self.duration:
                    break
        except Exception as e:
            print(f"An error occurred during recording: {e}")
        finally:
            self.stop()

    def stop(self):
        if self.open:
            self.open = False
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            self.audio.terminate()
            print("Recording complete!")

            print(f"Saving recording to: {self.full_path}")

            with wave.open(self.full_path, 'wb') as waveFile:
                waveFile.setnchannels(self.channels)
                waveFile.setsampwidth(self.audio.get_sample_size(self.format))
                waveFile.setframerate(self.rate)
                waveFile.writeframes(b''.join(self.audio_frames))
            print("Recording saved successfully!")

    def start(self):
        self.thread = threading.Thread(target=self.record)
        self.thread.start()
        self.thread.join()  # This will make the start method block until recording is complete

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.thread and self.thread.is_alive():
            self.stop()
            self.thread.join()
