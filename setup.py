from setuptools import setup, find_packages

setup(
    name='audio_recorder',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyaudio',
    ],
)
