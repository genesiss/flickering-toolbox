#!/usr/bin/env python

from src import SSVEPExperiment, SSVEPConfig

# Configure the experiment
config = SSVEPConfig()
config.N_STIM = 9               # Number of flickering stimuli
config.DURATION_S = 10.0         # Experiment duration in seconds
config.REFRESH_RATE = 60.0      # Monitor refresh rate

# Create and run the experiment
print("Starting SSVEP experiment...")
experiment = SSVEPExperiment(config)
report = experiment.run()
experiment.close()

