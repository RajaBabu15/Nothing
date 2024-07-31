# Audio Recorder

This project is a simple audio recording utility using Python. It allows you to record audio, save it to a specified directory, and supports custom callbacks for processing audio frames during recording.

## Features

- Record audio with specified parameters (rate, channels, format, etc.).
- Save recorded audio to a specified directory with unique filenames.
- Support for custom frame and stop callbacks.
- Multi-threaded recording to ensure non-blocking operations.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/RajaBabu15/Nothing.git
cd Nothing
```

2. Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:

```sh
pip install -r requirements.txt
```

4. Install the package in editable mode:

```sh
pip install -e .
```

## Usage

### Recording Audio

You can use the `AudioRecorder` class to record audio and save it to a specified directory. Here is an example:

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

### Running Tests

To run the tests, execute the `TestAudioRecorder.py` script:

```sh
python tests/TestAudioRecorder.py
```

### Directory Setup

Make sure to create a directory for recordings if it doesn't already exist. The `AudioRecorder` class will ensure the directory exists before saving the file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/RajaBabu15/Nothing).
