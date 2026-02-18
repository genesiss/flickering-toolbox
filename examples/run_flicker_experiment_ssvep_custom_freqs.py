#!/usr/bin/env python
"""
SSVEP experiment with custom frequencies.

This example demonstrates how to specify your own flicker frequencies
instead of using the auto-calculated ones.
"""

from src import SSVEPExperiment, SSVEPConfig

# Configure the experiment
config = SSVEPConfig()

# Specify custom frequencies in Hz
# These frequencies should ideally divide the REFRESH_RATE evenly for stable timing
config.CUSTOM_FREQUENCIES = [15.0, 12.0, 10.0, 8.57]  # 4 stimuli with specific frequencies
config.REFRESH_RATE = 60.0      
config.DURATION_S = 10.0        
config.FULLSCREEN = True        
config.SHOW_LABELS = True

# Note: N_STIM is automatically set to len(CUSTOM_FREQUENCIES)
# Note: MIN_FRAMES_PER_CYCLE is ignored when using CUSTOM_FREQUENCIES

# Create and run the experiment
print("Starting SSVEP experiment with custom frequencies...")
print(f"Frequencies: {config.CUSTOM_FREQUENCIES}")
experiment = SSVEPExperiment(config)
report = experiment.run()
experiment.close()
