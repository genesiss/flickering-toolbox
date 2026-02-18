#!/usr/bin/env python
"""
Example: Using Gabor patches as custom stimuli.

This demonstrates how to use Gabor patches as flickering stimuli.
"""

from psychopy import visual
from src import SSVEPExperiment, SSVEPConfig

def create_gabor_off(win, pos, size, index):
    return visual.GratingStim(
        win,
        tex='sin',
        mask='gauss',
        pos=pos,
        size=size,
        sf=4,
        ori=0,
        contrast=0.2,        # Low contrast for OFF state
        phase=0
    )

def create_gabor_oriented(win, pos, size, index):
    orientations = [0, 45, 90, 135, 0, 45, 90, 135, 0]  # One per stimulus
    return visual.GratingStim(
        win,
        tex='sin',
        mask='gauss',
        pos=pos,
        size=size,
        sf=4,
        ori=orientations[index],  # Different orientation per position
        contrast=1.0,
        phase=0
    )

config = SSVEPConfig()
config.N_STIM = 9
config.DURATION_S = 5.0
config.STIM_SIZE = 0.25
config.SHOW_LABELS = True

# Same Gabor for ON state, different orientations
config.CUSTOM_STIM_ON = create_gabor_oriented
config.CUSTOM_STIM_OFF = create_gabor_off

experiment = SSVEPExperiment(config)
experiment.run()
experiment.close()