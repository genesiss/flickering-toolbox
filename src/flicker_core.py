import math
import numpy as np
from scipy.signal import max_len_seq

def calculate_frequencies(refresh_rate: float, min_frames_per_cycle: int, n_stim: int):
    """
    Generate flicker frequencies based on refresh rate constraints.
    
    Args:
        refresh_rate: Monitor refresh rate in Hz (e.g., 60.0, 120.0, 240.0)
        min_frames_per_cycle: Minimum frames per cycle, controls maximum frequency
                             (e.g., min_frames=3 at 60Hz gives max freq of 20Hz)
        n_stim: Number of stimuli requiring unique frequencies
    
    Returns:
        List of n_stim frequencies in Hz, sorted from highest to lowest
    
    Raises:
        AssertionError: If parameters are invalid or n_stim is too large for the
                       given refresh_rate and min_frames_per_cycle combination
    
    Example:
        >>> freqs = calculate_frequencies(60.0, 3, 5)
        >>> print(freqs)
        [20.0, 15.0, 12.0, 10.0, 8.571428571428571]
        
        At 60Hz with min_frames=3:
        - First freq: 60/3 = 20Hz (3 frames/cycle)
        - Second freq: 60/4 = 15Hz (4 frames/cycle)
        - Third freq: 60/5 = 12Hz (5 frames/cycle)
    """

    assert refresh_rate > 0, f"refresh_rate must be bigger than zero. Provided value: {refresh_rate}"
    assert min_frames_per_cycle > 1, f"min_frames_per_cycle must be bigger than one. Provided value: {min_frames_per_cycle}"
    assert n_stim > 0, f"n_stim must be bigger than zero. Provided value: {n_stim}"

    divisors = list(range(min_frames_per_cycle, int(refresh_rate) + 1))  # min_frames_per_cycle..refresh_rate

    assert (refresh_rate - min_frames_per_cycle+1) >= n_stim, f"Too many stimuli provided for given refresh_rate and min_frames_per_cycle. Maximum number of allowed stimuli is {len(divisors)}."

    stable_freqs = [refresh_rate / d for d in divisors] # calculate possible frequencies based on REFRESH_RATE
    return stable_freqs[:n_stim] # choose first N_STIM frequencies

def calculate_cycle_params(refresh_rate: float, freq: float, duty_cycle: float):
    """
    Convert frequency to frame-based cycle parameters.
    
    Calculates how many frames constitute one complete flicker cycle and
    how many of those frames the stimulus should be ON.
    
    Args:
        refresh_rate: Monitor refresh rate in Hz
        freq: Target flicker frequency in Hz
        duty_cycle: Ratio of ON time (0.0 to 1.0)
                   - 0.5 = 50% ON, 50% OFF
                   - 0.25 = 25% ON, 75% OFF
                   - 0.75 = 75% ON, 25% OFF
    
    Returns:
        Tuple of (frames_per_cycle, on_frames):
        - frames_per_cycle: Total frames in one complete cycle
        - on_frames: Number of frames stimulus is ON (guaranteed ≥1 and < frames_per_cycle)
    
    Example:
        >>> frames, on = calculate_cycle_params(60.0, 10.0, 0.5)
        >>> print(f"{frames} frames/cycle: {on} ON, {frames-on} OFF")
        6 frames/cycle: 3 ON, 3 OFF
        
        >>> frames, on = calculate_cycle_params(120.0, 20.0, 0.25)
        >>> print(f"{frames} frames/cycle: {on} ON, {frames-on} OFF")
        6 frames/cycle: 2 ON, 4 OFF
    """
    frames_per_cycle = int(round(refresh_rate / freq))  # calculate number of frames for some frequency
    on_frames = int(round(frames_per_cycle * duty_cycle)) # calculate number of "on" frames, based on DUTY_CYCLE
    on_frames = max(1, min(on_frames, frames_per_cycle - 1)) # make sure that there is some flickering by ensuring we have at least 1 on frame and at least 1 off frame
    return frames_per_cycle, on_frames

def generate_positions(n_stim: int):
    """
    Generate grid positions for stimuli layout.
    
    Args:
        n_stim: Number of stimuli to position
    
    Returns:
        List of (x, y) tuples in normalized coordinates (-1 to 1)
        Positions are ordered left-to-right, top-to-bottom
    
    Example:
        >>> positions = generate_positions(4)
        >>> # Creates 2x2 grid:
        >>> # [-0.5, 0.5]  [ 0.5, 0.5]
        >>> # [-0.5,-0.5]  [ 0.5,-0.5]
    """
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

def generate_frame_pattern(frames_per_cycle: int, on_frames: int):
    """
    Generate binary ON/OFF pattern for one cycle of SSVEP stimulation.
    
    Args:
        frames_per_cycle: Number of frames in one complete cycle
        on_frames: Number of frames stimulus is ON per cycle
    
    Returns:
        List of binary values (0 or 1) indicating OFF/ON state for each frame in one cycle
        Length equals frames_per_cycle
    
    Example:
        >>> pattern = generate_frame_pattern(4, 2)
        >>> print(pattern)
        [1, 1, 0, 0]
        # 4 frames/cycle: 2 ON, 2 OFF
        # To use: pattern[frameN % len(pattern)]
    """
    pattern = [1 if i < on_frames else 0 for i in range(frames_per_cycle)]
    return pattern

def calculate_m_sequences(n_stim: int, nbits: int = 6, shift_step: int = 4):
    """
    Generate m-sequences for c-VEP stimulation.
    
    Args:
        n_stim: Number of stimuli
        nbits: Number of bits to use. Length of the resulting sequence will be (2**nbits) - 1.
               In case of 6, the length is 63.
        shift_step: Shift step of some stimuli. T(k) = shift_step * k ; k=0,1...n_stim
    
    Returns:
        List of m-sequence patterns, one for each stimulus
    """
    base_seq, _ = max_len_seq(nbits=nbits)

    patterns = []
    for s in range(n_stim):
        shift = s * shift_step
        shifted_seq = np.roll(base_seq, shift)
        patterns.append(shifted_seq)

    return patterns
