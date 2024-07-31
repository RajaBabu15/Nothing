import cv2
import threading
import time
import os
from common.file_management import get_unique_filename, create_output_directory
from common.config import VIDEO_SETTINGS, OUTPUT_DIRECTORIES
from common.exceptions import VideoRecorderError

class VideoRecorder:
    def __init__(self, filename="temp_video.avi", directory=None, frame_callback=None, duration=10, stop_callback=None, show_viewframe=True, viewframe_title="Video Frame"):
        self.open = False
        self.device_index = VIDEO_SETTINGS['device_index']
        self.fps = VIDEO_SETTINGS['fps']
        self.frame_size = VIDEO_SETTINGS['frame_size']
        self.directory = directory or OUTPUT_DIRECTORIES['video']
        
        create_output_directory(self.directory)
        self.filename = get_unique_filename(filename, self.directory)
        self.full_path = os.path.join(self.directory, self.filename)
        self.frame_callback = frame_callback
        self.duration = duration
        self.stop_callback = stop_callback
        self.show_viewframe = show_viewframe
        self.viewframe_title = viewframe_title
        self.video_cap = cv2.VideoCapture(self.device_index)
        self.video_writer = cv2.VideoWriter_fourcc(*VIDEO_SETTINGS['codec'])
        self.video_stream = None
        self.frame_counts = 1
        self.thread = None

    def record(self):
        try:
            self.video_stream = cv2.VideoWriter(self.full_path, self.video_writer, self.fps, self.frame_size)
            self.open = True
            start_time = time.time()

            print("Video Recording Started")
            while self.open:
                ret, video_frame = self.video_cap.read()
                elapsed_time = time.time() - start_time
                if not ret:
                    break

                video_frame = cv2.cvtColor(cv2.flip(video_frame, 1), cv2.COLOR_BGR2RGB)
                video_frame.flags.writeable = False

                if self.frame_callback:
                    video_frame = self.frame_callback(video_frame, self.frame_counts, elapsed_time)

                video_frame.flags.writeable = True
                video_frame = cv2.cvtColor(video_frame, cv2.COLOR_RGB2BGR)
                self.video_stream.write(video_frame)
                self.frame_counts += 1

                if self.show_viewframe:
                    cv2.imshow(self.viewframe_title, video_frame)

                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

                if self.stop_callback and self.stop_callback(video_frame, self.frame_counts, elapsed_time):
                    break

                if not self.stop_callback and elapsed_time >= self.duration:
                    break

        except Exception as e:
            raise VideoRecorderError(f"An error occurred during video recording: {e}")

        finally:
            self.stop()

    def stop(self):
        if self.open:
            self.open = False
            if self.video_stream:
                self.video_stream.release()
                self.video_cap.release()
            cv2.destroyAllWindows()
            print(f"Video Recording complete! Saving to: {self.full_path}")
            print("Video Recording saved successfully!")

    def start(self):
        self.thread = threading.Thread(target=self.record)
        self.thread.start()

    def join(self):
        self.thread.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.thread and self.thread.is_alive():
            self.stop()
            self.thread.join()
