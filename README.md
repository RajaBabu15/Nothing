# Audio and Video Recorder

This repository contains two Python utilities: an **Audio Recorder** and a **Video Recorder**. Both tools provide simple interfaces for recording audio and video, respectively, with support for custom callbacks and non-blocking operations.

## Features

### Audio Recorder

- Record audio with specified parameters (rate, channels, format, etc.).
- Save recorded audio to a specified directory with unique filenames.
- Support for custom frame and stop callbacks.
- Multi-threaded recording to ensure non-blocking operations.

### Video Recorder

- Record video with specified parameters (device index, fps, frame size, etc.).
- Save recorded video to a specified directory with unique filenames.
- Support for custom frame and stop callbacks.
- Multi-threaded recording to ensure non-blocking operations.

## Project Structure

```
audio_video_recorder/
├── .conda/
├── audio_recorder.egg-info/
├── docs/
├── notebooks/
├── scripts/
├── src/
│   ├── audio_recorder/
│   │   ├── __init__.py
│   │   ├── recorder.py
│   │   └── utils.py
│   ├── video_recorder/
│   │   ├── __init__.py
│   │   ├── recorder.py
│   │   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── TestAudioRecorder.py
│   └── TestVideoRecorder.py
├── __pycache__/
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

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

Use the `AudioRecorder` class to record audio and save it to a specified directory. Here is an example:

```python
from src.audio_recorder.recorder import AudioRecorder

# Record for 5 seconds and save to a different directory
with AudioRecorder(filename="my_audio.wav", duration=5, directory="my_recordings") as recorder:
    pass

# Or, if you want to use a custom stop callback:
def stop_on_loud_sound(data, frames_per_buffer, elapsed_time, audio_frames):
    # This is just an example. You'd need to implement actual loudness detection.
    return max(abs(int.from_bytes(data, byteorder='little', signed=True)) for _ in range(frames_per_buffer)) > 1000

recorder = AudioRecorder(filename="loud_sound.wav", stop_callback=stop_on_loud_sound, directory="my_recordings")
recorder.start()
```

### Recording Video

Use the `VideoRecorder` class to record video and save it to a specified directory. Here is an example:

```python
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
```

### Running Tests

To run the tests for both the audio and video recorders, execute the respective test scripts:

```sh
# For Audio Recorder
python tests/TestAudioRecorder.py

# For Video Recorder
python tests/TestVideoRecorder.py
```

### Directory Setup

Ensure the directory for recordings exists. Both `AudioRecorder` and `VideoRecorder` classes will check and create the directory if it doesn't exist before saving the files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/RajaBabu15/Nothing).

