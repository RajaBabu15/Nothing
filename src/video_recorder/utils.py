import os
import logging

def get_unique_filename(filename, directory="videos"):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = os.path.join(directory, filename)
    while os.path.exists(new_filename):
        new_filename = os.path.join(directory, f"{base}_{counter}{extension}")
        counter += 1
    return new_filename

def create_output_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    logging.info(f"Created directory: {directory}")
