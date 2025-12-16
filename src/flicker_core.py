import math
import numpy as np
from scipy.signal import max_len_seq
from psychopy import visual, core, logging


def calculate_frequencies(refresh_rate: float, min_frames_per_cycle: int, n_stim: int):

    assert refresh_rate > 0, f"refresh_rate must be bigger than zero. Provided value: {refresh_rate}"
    assert min_frames_per_cycle > 0, f"min_frames_per_cycle must be bigger than zero. Provided value: {min_frames_per_cycle}"
    assert n_stim > 0, f"n_stim must be bigger than zero. Provided value: {n_stim}"
    assert (refresh_rate - min_frames_per_cycle+1) >= n_stim, f"Too many stimuli provided for given refresh_rate and min_frames_per_cycle. Maximum number of allowed stimuli is {(refresh_rate - min_frames_per_cycle+1)}"

    divisors = list(range(min_frames_per_cycle, int(refresh_rate) + 1))  # min_frames_per_cycle..refresh_rate
    stable_freqs = [refresh_rate / d for d in divisors] # calculate possible frequencies based on REFRESH_RATE
    return stable_freqs[:n_stim] # choose first N_STIM frequencies

def calculate_cycle_params(refresh_rate: float, freq: float, duty_cycle: float):
    frames_per_cycle = int(round(refresh_rate / freq))  # calculate number of frames for some frequency
    on_frames = int(round(frames_per_cycle * duty_cycle)) # calculate number of "on" frames, based on DUTY_CYCLE
    on_frames = max(1, min(on_frames, frames_per_cycle - 1)) # make sure that there is some flickering by ensuring we have at least 1 on frame and at least 1 off frame
    return frames_per_cycle, on_frames

def generate_positions(n_stim: int):
    cols = math.ceil(math.sqrt(n_stim))
    rows = math.ceil(n_stim / cols)
    spacing_x = 1.0 / (cols - 1) if cols > 1 else 0
    spacing_y = 1.0 / (rows - 1) if rows > 1 else 0

    positions = []
    for r in range(rows):
        for c in range(cols):
            if len(positions) == n_stim:
                break
            x = (c - (cols - 1)/2) * spacing_x
            y = ((rows - 1)/2 - r) * spacing_y
            positions.append((x, y))
    return positions

def generate_frame_pattern(frames_per_cycle: int, on_frames: int, total_frames: int):
    pattern = []
    for frameN in range(total_frames):
        cycle_pos = frameN % frames_per_cycle
        pattern.append(1 if cycle_pos < on_frames else 0)
    return pattern

def calculate_m_sequences(n_stim: int):
    nbits = 6 # Number of bits to use. Length of the resulting sequence will be (2**nbits) - 1. In case of 6, the lenght is 63.
    shift_step = 4 # Shift step of some stimuli. T(k) = 4xK ; k=0,1...n_stim
    base_seq, state = max_len_seq(nbits=nbits)

    patterns = []
    # generate shifted patterns for all stimuli
    for s in range(n_stim):
        shift = s * shift_step
        shifted_seq = np.roll(base_seq, shift)
        logging.info(shifted_seq)
        patterns.append(shifted_seq)

    return patterns
