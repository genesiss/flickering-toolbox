#!/usr/bin/env python
"""
Example: Mixing different types of stimuli.

This demonstrates how to use different stimulus types in the same experiment
by using the index parameter to select the appropriate type.
"""

from psychopy import visual
from src import SSVEPExperiment, SSVEPConfig

STIMULUS_TYPES = {
    0: lambda win, pos, size: visual.Circle(
        win, radius=size/2, pos=pos, 
        fillColor='red', lineColor='white', lineWidth=2
    ),
    1: lambda win, pos, size: visual.Rect(
        win, width=size, height=size, pos=pos,
        fillColor='green', lineColor='white', lineWidth=2
    ),
    2: lambda win, pos, size: visual.GratingStim(
        win, tex='sin', mask='gauss', pos=pos, 
        size=size, sf=4, ori=0, contrast=1.0
    ),
    3: lambda win, pos, size: visual.TextStim(
        win, text='X', pos=pos, height=size * 0.6,
        color='yellow', bold=True
    ),
}

# Default stimulus for undefined indices
DEFAULT_STIM = lambda win, pos, size: visual.Circle(
    win, radius=size/2, pos=pos,
    fillColor='blue', lineColor='white', lineWidth=2
)

def create_mixed_stim_on(win, pos, size, index):
    creator = STIMULUS_TYPES.get(index, DEFAULT_STIM)
    return creator(win, pos, size)

def create_invisible(win, pos, size, index):
    """Create invisible stimulus for OFF state."""
    return visual.Rect(
        win, width=size, height=size, pos=pos,
        fillColor=[0, 0, 0], lineColor=None
    )

# Mix different stimulus types
print("Example: Mixed stimulus types")

config = SSVEPConfig()
config.N_STIM = 9
config.DURATION_S = 5.0
config.STIM_SIZE = 0.3
config.SHOW_LABELS = True
config.BACKGROUND_COLOR = [0, 0, 0]

config.CUSTOM_STIM_ON = create_mixed_stim_on
config.CUSTOM_STIM_OFF = create_invisible  # All OFF states invisible

experiment = SSVEPExperiment(config)
report = experiment.run()
experiment.close()
