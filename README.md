# Audio and Video Recorder

This repository contains two Python utilities: an **Audio Recorder** and a **Video Recorder**. Both tools provide simple interfaces for recording audio and video, respectively, with support for custom callbacks and non-blocking operations.

## Features

### Audio Recorder

- **Configurable Recording Parameters**: Record audio with custom settings, including rate, channels, format, etc.
- **Unique File Saving**: Save recorded audio to a specified directory with unique filenames.
- **Custom Callbacks**: Implement custom frame and stop callbacks for advanced control over recording.
- **Multi-threaded**: Utilize multi-threaded recording to ensure non-blocking operations.

### Video Recorder

- **Configurable Recording Parameters**: Record video with specified settings, including device index, fps, frame size, etc.
- **Unique File Saving**: Save recorded video to a specified directory with unique filenames.
- **Custom Callbacks**: Implement custom frame and stop callbacks for advanced control over recording.
- **Multi-threaded**: Utilize multi-threaded recording to ensure non-blocking operations.

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/RajaBabu15/Nothing.git
   cd Nothing
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Install the package in editable mode:**

   ```sh
   pip install -e .
   ```

## Usage

### Recording Audio

The `AudioRecorder` class is designed to simplify audio recording while providing options for customization. Here's how you can record audio:

```python
from src.audio_recorder.recorder import AudioRecorder

# Basic audio recording for 5 seconds, saved to a custom directory
with AudioRecorder(filename="my_audio.wav", duration=5, directory="my_recordings") as recorder:
    pass

# Using a custom stop callback to stop recording based on loudness
def stop_on_loud_sound(data, frames_per_buffer, elapsed_time, audio_frames):
    # Example logic for detecting loudness
    return max(abs(int.from_bytes(data, byteorder='little', signed=True)) for _ in range(frames_per_buffer)) > 1000

recorder = AudioRecorder(filename="loud_sound.wav", stop_callback=stop_on_loud_sound, directory="my_recordings")
recorder.start()
```

### Recording Video

The `VideoRecorder` class provides a straightforward interface for video recording. Here's a simple usage example:

```python
from src.video_recorder.recorder import VideoRecorder

# Basic video recording for 5 seconds, saved to a custom directory
with VideoRecorder(filename="my_video.avi", duration=5, directory="my_recordings") as recorder:
    pass

# Using a custom stop callback to stop recording after a certain number of frames
def stop_on_motion(video_frame, frame_counts, elapsed_time):
    # Example logic to stop recording after 100 frames
    return frame_counts > 100

recorder = VideoRecorder(filename="motion_detection.avi", stop_callback=stop_on_motion, directory="my_recordings")
recorder.start()
recorder.join()
```

### Running Tests

To ensure everything works as expected, run the tests for both audio and video recorders:

```sh
# For Audio Recorder
python tests/TestAudioRecorder.py

# For Video Recorder
python tests/TestVideoRecorder.py
```

### Directory Setup

Before recording, ensure that the directory for recordings exists. The `AudioRecorder` and `VideoRecorder` classes will automatically create the directory if it doesn't exist before saving the files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/RajaBabu15/Nothing).
