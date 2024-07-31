import os
import logging
import time

def get_unique_filename(filename, directory):
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

def remove_old_files(directory, days=30):
    """Remove files older than a certain number of days."""
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and os.path.getmtime(filepath) < time.time() - days * 86400:
            os.remove(filepath)
            logging.info(f"Removed old file: {filepath}")
