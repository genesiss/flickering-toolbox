#!/usr/bin/env python
"""
This example demonstrates how to use the FLIP_CALLBACK feature.

The callback receives:
- frame_number: Current frame index (0, 1, 2, ...)
- timestamp: Exact flip time from PsychoPy
"""

from src import SSVEPExperiment, SSVEPConfig
from psychopy import logging

def log_flip_times(frame_num, timestamp):
    """Log each flip time to console."""
    logging.info(f"Frame {frame_num}: flip at {timestamp:.4f}s")


config = SSVEPConfig()
config.N_STIM = 9               
config.DURATION_S = 10.0        
config.REFRESH_RATE = 60.0
config.FLIP_CALLBACK = log_flip_times  # Set the flip callback

experiment = SSVEPExperiment(config)
report = experiment.run()
experiment.close()


