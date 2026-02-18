#!/usr/bin/env python
from psychopy import visual
from src import SSVEPExperiment, SSVEPConfig, CVEPExperiment, CVEPConfig

keyboard_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

def create_letter_on(win, pos, size, index):
    """Create bright letter stimulus (ON state)."""
    return visual.TextStim(
        win,
        text=keyboard_letters[index],
        pos=pos,
        height=size * 0.6,
        color='white',
        bold=True
    )

def create_letter_off(win, pos, size, index):
    """Create dim letter stimulus (OFF state)."""
    return visual.TextStim(
        win,
        text=keyboard_letters[index],
        pos=pos,
        height=size * 0.6,
        color=[0.3, 0.3, 0.3],
        bold=True
    )

config = CVEPConfig()
config.N_STIM = 9
config.DURATION_S = 10.0
config.STIM_SIZE = 0.25
config.SHOW_LABELS = True
config.BACKGROUND_COLOR = [0, 0, 0]

config.CUSTOM_STIM_ON = create_letter_on
config.CUSTOM_STIM_OFF = create_letter_off

experiment = CVEPExperiment(config)
report = experiment.run()
experiment.close()
