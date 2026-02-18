#!/usr/bin/env python

from src import CVEPExperiment, CVEPConfig

# Configure the experiment
config = CVEPConfig()
config.N_STIM = 9               # Number of flickering stimuli
config.DURATION_S = 10.0         # Experiment duration in seconds
config.REFRESH_RATE = 60.0      # Monitor refresh rate (MUST match your display!)
config.NBITS = 6                # m-sequence length = 2^6 - 1 = 63 frames
config.SHIFT_STEP = 4           # Circular shift between stimuli
config.FULLSCREEN = True        # Run in fullscreen mode
config.SHOW_LABELS = True       # Display stimulus indices

# Create and run the experiment
print("Starting c-VEP experiment...")
experiment = CVEPExperiment(config)
report = experiment.run()
experiment.close()
