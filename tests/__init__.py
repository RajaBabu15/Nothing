# tests/__init__.py

import unittest
import logging

# Configure logging for the test suite
logging.basicConfig(level=logging.INFO)

# Initialize any global resources needed for testing
def setup_package():
    logging.info("Setting up the test package.")

def teardown_package():
    logging.info("Tearing down the test package.")
