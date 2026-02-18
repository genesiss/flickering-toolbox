# API Reference: Core Functions

Pure computational functions from `flicker_core.py`.

These functions have no PsychoPy dependencies and can be used standalone.

## calculate_frequencies

Generate stable flicker frequencies based on refresh rate constraints.

```python
from src import calculate_frequencies

frequencies = calculate_frequencies(
    refresh_rate, 
    min_frames_per_cycle, 
    n_stim
)
```

### Parameters

- **refresh_rate** (`float`): Monitor refresh rate in Hz (e.g., 60.0, 120.0, 240.0)
- **min_frames_per_cycle** (`int`): Minimum frames per cycle, controls maximum frequency
- **n_stim** (`int`): Number of stimuli requiring unique frequencies

### Returns

- **List[float]**: List of `n_stim` frequencies in Hz, sorted from highest to lowest

### Raises

- **AssertionError**: If parameters are invalid or `n_stim` is too large for the given `refresh_rate` and `min_frames_per_cycle` combination

### Example

```python
>>> freqs = calculate_frequencies(60.0, 3, 5)
>>> print(freqs)
[20.0, 15.0, 12.0, 10.0, 8.571428571428571]
```

At 60Hz with `min_frames=3`:    
- First freq: 60/3 = 20Hz (3 frames/cycle)  
- Second freq: 60/4 = 15Hz (4 frames/cycle)     
- Third freq: 60/5 = 12Hz (5 frames/cycle)  

---

## calculate_cycle_params

Convert frequency to frame-based cycle parameters.

```python
from src import calculate_cycle_params

frames_per_cycle, on_frames = calculate_cycle_params(
    refresh_rate,
    freq,
    duty_cycle
)
```

### Parameters

- **refresh_rate** (`float`): Monitor refresh rate in Hz
- **freq** (`float`): Target flicker frequency in Hz
- **duty_cycle** (`float`): Ratio of ON time (0.0 to 1.0)
  - `0.5` = 50% ON, 50% OFF
  - `0.25` = 25% ON, 75% OFF
  - `0.75` = 75% ON, 25% OFF

### Returns

- **Tuple[int, int]**: `(frames_per_cycle, on_frames)`
  - `frames_per_cycle`: Total frames in one complete cycle
  - `on_frames`: Number of frames stimulus is ON (guaranteed ≥1 and < frames_per_cycle)

### Example

```python
>>> frames, on = calculate_cycle_params(60.0, 10.0, 0.5)
>>> print(f"{frames} frames/cycle: {on} ON, {frames-on} OFF")
6 frames/cycle: 3 ON, 3 OFF

>>> frames, on = calculate_cycle_params(120.0, 20.0, 0.25)
>>> print(f"{frames} frames/cycle: {on} ON, {frames-on} OFF")
6 frames/cycle: 2 ON, 4 OFF
```

### Notes

Due to integer frame counts, actual duty cycle may differ slightly from requested. The function ensures at least 1 ON frame and at least 1 OFF frame.

---

## generate_positions

Generate grid positions for stimulus layout.

```python
from src import generate_positions

positions = generate_positions(n_stim)
```

### Parameters

- **n_stim** (`int`): Number of stimuli to position

### Returns

- **List[Tuple[float, float]]**: List of `(x, y)` tuples in normalized coordinates (-1 to 1). Positions are ordered left-to-right, top-to-bottom.

### Example

```python
>>> positions = generate_positions(4)
>>> # Creates 2x2 grid:
>>> # [-0.5, 0.5]  [ 0.5, 0.5]
>>> # [-0.5,-0.5]  [ 0.5,-0.5]
```

## generate_frame_pattern

Generate binary ON/OFF pattern for one cycle of SSVEP stimulation.

```python
from src import generate_frame_pattern

pattern = generate_frame_pattern(
    frames_per_cycle,
    on_frames
)
```

### Parameters

- **frames_per_cycle** (`int`): Number of frames in one complete cycle
- **on_frames** (`int`): Number of frames stimulus is ON per cycle

### Returns

- **List[int]**: Binary values (0 or 1) indicating OFF/ON state for each frame in one cycle. Length equals `frames_per_cycle`.

### Example

```python
>>> pattern = generate_frame_pattern(4, 2)
>>> print(pattern)
[1, 1, 0, 0]
# 4 frames/cycle: 2 ON, 2 OFF
# To use: pattern[frameN % len(pattern)]

>>> pattern = generate_frame_pattern(6, 3)
>>> print(pattern)
[1, 1, 1, 0, 0, 0]
# One cycle: 3 ON, 3 OFF
```

### Notes

Returns pattern for ONE cycle only. Use modulo indexing (`frameN % len(pattern)`) to repeat across experiment duration. This is more memory-efficient than generating the full experiment-length pattern.

---

## calculate_m_sequences

Generate m-sequences for c-VEP stimulation.

```python
from src import calculate_m_sequences

patterns = calculate_m_sequences(
    n_stim,
    nbits=6,
    shift_step=4
)
```

### Parameters

- **n_stim** (`int`): Number of stimuli
- **nbits** (`int`, optional): Number of bits for m-sequence. Length of resulting sequence will be `(2**nbits) - 1`. Default: 6 (length 63)
- **shift_step** (`int`, optional): Shift step between stimuli. Pattern k uses shift `k * shift_step`. Default: 4

### Returns

- **List[numpy.ndarray]**: List of m-sequence patterns, one for each stimulus. Each pattern is a binary numpy array of length `2**nbits - 1`.

### Example

```python
>>> patterns = calculate_m_sequences(4, nbits=6, shift_step=4)
>>> len(patterns)
4
>>> len(patterns[0])
63
>>> patterns[0][:10]
array([1, 0, 1, 1, 1, 0, 1, 0, 0, 1])
```

## See Also

- [Examples](examples.md) - Usage examples