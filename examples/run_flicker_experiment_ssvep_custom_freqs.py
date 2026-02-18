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
config.REFRESH_RATE = 60.0      # Monitor refresh rate (MUST match your display!)
config.DURATION_S = 10.0        # Experiment duration in seconds
config.FULLSCREEN = True        # Run in fullscreen mode
config.SHOW_LABELS = True       # Display frequency labels

# Note: N_STIM is automatically set to len(CUSTOM_FREQUENCIES)
# Note: MIN_FRAMES_PER_CYCLE is ignored when using CUSTOM_FREQUENCIES

# Create and run the experiment
print("Starting SSVEP experiment with custom frequencies...")
print(f"Frequencies: {config.CUSTOM_FREQUENCIES}")
experiment = SSVEPExperiment(config)
report = experiment.run()
experiment.close()

print(f"\nExperiment completed!")
print(f"Stability: {report['stability_percent']:.2f}%")
print(f"Dropped frames: {report['dropped_frames']}")
