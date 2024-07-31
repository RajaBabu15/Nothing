import pyaudio
import wave
import threading
import time
import os

class AudioRecorder:
    def __init__(self, rate=44100, frames_per_buffer=1024, channels=2, format=pyaudio.paInt16, filename="temp_audio.wav", frame_callback=None):
        self.open = False
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.channels = channels
        self.format = format
        self.filename = filename
        self.filename = self._get_unique_filename(self.filename)
        self.frame_callback = frame_callback
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.audio_frames = []
        self.start_time = time.time()

    def _get_unique_filename(self, filename):
        base, extension = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        while os.path.exists(new_filename):
            new_filename = f"{base}_{counter}{extension}"
            counter += 1
        return new_filename

    def record(self, stop_callback=None):
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.stream.start_stream()
        self.open = True
        start_time = time.time()

        try:
            if self.open:
                print("Recording...")
                self.audio_frames.clear()
            while self.open:
                data = self.stream.read(self.frames_per_buffer)
                self.audio_frames.append(data)

                if self.frame_callback:
                    self.frame_callback(data, self.frames_per_buffer, time.time() - start_time, self.audio_frames)

                if stop_callback and stop_callback(data, self.frames_per_buffer, time.time() - start_time, self.audio_frames):
                    break

                if not stop_callback and (time.time() - start_time) >= 10:
                    break
        except Exception:
            print("Error recording audio.")
            pass
        finally:
            self.stop()

    def stop(self):
        if self.open:
            self.open = False
            try:
                if self.stream:
                    self.stream.stop_stream()
                    self.stream.close()
                self.audio.terminate()
            except Exception:
                print("Error stopping audio stream.")
                pass

            try:
                with wave.open(self.filename, 'wb') as waveFile:
                    waveFile.setnchannels(self.channels)
                    waveFile.setsampwidth(self.audio.get_sample_size(self.format))
                    waveFile.setframerate(self.rate)
                    waveFile.writeframes(b''.join(self.audio_frames))
                    print("Recording Completed... "+self.filename)
            except Exception:
                print("Error saving recording to file.")
                pass

    def start(self, stop_callback=None):
        self.thread = threading.Thread(target=self.record, args=(stop_callback,))
        self.thread.start()

    def join(self):
        self.thread.join()