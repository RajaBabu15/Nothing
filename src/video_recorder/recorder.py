import cv2
import threading
import time
import logging
from .utils import get_unique_filename, create_output_directory

class VideoRecorder:
    def __init__(self, device_index=0, fps=6, frame_size=(640, 480), filename="temp_video.avi", frame_callback=None, directory="videos"):
        """
        Initializes the VideoRecorder.
        
        Parameters:
            device_index (int): Index of the video capture device.
            fps (int): Frames per second for the recording.
            frame_size (tuple): Frame size for the recording.
            filename (str): Name of the output video file.
            frame_callback (callable): Callback function to process each frame.
            directory (str): Directory where the video will be saved.
        """
        self.open = True
        self.device_index = device_index
        self.fps = fps
        self.frame_size = frame_size
        self.filename = get_unique_filename(filename, directory)
        self.frame_callback = frame_callback
        self.directory = directory
        self.video_cap = cv2.VideoCapture(self.device_index)
        self.video_writer = cv2.VideoWriter_fourcc(*"MJPG")
        create_output_directory(self.directory)
        self.video_out = cv2.VideoWriter(self.filename, self.video_writer, self.fps, self.frame_size)
        self.frame_counts = 1
        self.start_time = time.time()
        self.thread = None

    def record(self, stop_callback=None):
        """
        Records video until the stop condition is met.
        
        Parameters:
            stop_callback (callable): Callback function to decide when to stop recording.
        """
        start_time = time.time()

        while self.open:
            ret, video_frame = self.video_cap.read()
            if not ret:
                logging.error("Failed to read video frame.")
                break

            video_frame = cv2.cvtColor(cv2.flip(video_frame, 1), cv2.COLOR_BGR2RGB)
            video_frame.flags.writeable = False

            if self.frame_callback:
                video_frame = self.frame_callback(video_frame, self.frame_counts, time.time() - start_time)

            video_frame.flags.writeable = True
            video_frame = cv2.cvtColor(video_frame, cv2.COLOR_RGB2BGR)

            self.video_out.write(video_frame)
            self.frame_counts += 1
            cv2.imshow('Video Frame', video_frame)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

            if stop_callback and stop_callback(video_frame, self.frame_counts, time.time() - start_time):
                break

            if not stop_callback and (time.time() - start_time) >= 5:
                break

        self.stop()

    def stop(self):
        """
        Stops the video recording and releases resources.
        """
        if self.open:
            self.open = False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()
            logging.info(f"Recording saved to: {self.filename}")

    def start(self, stop_callback=None):
        """
        Starts the video recording in a separate thread.
        
        Parameters:
            stop_callback (callable): Callback function to decide when to stop recording.
        """
        self.thread = threading.Thread(target=self.record, args=(stop_callback,))
        self.thread.start()

    def join(self):
        """
        Waits for the recording thread to finish.
        """
        self.thread.join()
