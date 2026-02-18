# Examples: Low-Level API

Using the core functions directly.

## Core Functions

Import the functions directly:

```python
from src import (
    calculate_frequencies,
    calculate_cycle_params,
    generate_positions,
    generate_frame_pattern,
    calculate_m_sequences
)
```

## Example 1: Calculate Frequencies

Generate stable flicker frequencies:

```python
from src import calculate_frequencies

# At 60Hz, min 3 frames/cycle, 6 stimuli
frequencies = calculate_frequencies(
    refresh_rate=60.0,
    min_frames_per_cycle=3,
    n_stim=6
)

print("Generated frequencies:")
for i, freq in enumerate(frequencies, 1):
    print(f"  Stimulus {i}: {freq:.2f} Hz")

# Output:
# Stimulus 1: 20.00 Hz (60/3)
# Stimulus 2: 15.00 Hz (60/4)
# Stimulus 3: 12.00 Hz (60/5)
# Stimulus 4: 10.00 Hz (60/6)
# Stimulus 5: 8.57 Hz (60/7)
# Stimulus 6: 7.50 Hz (60/8)
```

## Example 2: Calculate Cycle Parameters

Convert frequency to frame counts:

```python
from src import calculate_cycle_params

refresh_rate = 60.0
frequency = 15.0
duty_cycle = 0.5

frames_per_cycle, on_frames = calculate_cycle_params(
    refresh_rate, frequency, duty_cycle
)

print(f"Frequency: {frequency} Hz")
print(f"Frames per cycle: {frames_per_cycle}")
print(f"ON frames: {on_frames}")
print(f"OFF frames: {frames_per_cycle - on_frames}")
print(f"Reconstructed frequency: {refresh_rate / frames_per_cycle:.2f} Hz")

# Output:
# Frequency: 15.0 Hz
# Frames per cycle: 4
# ON frames: 2
# OFF frames: 2
# Reconstructed frequency: 15.00 Hz
```

## Example 3: Generate Grid Positions

Calculate stimulus positions:

```python
from src import generate_positions
import matplotlib.pyplot as plt

# Generate positions for 9 stimuli
positions = generate_positions(n_stim=9)

print("Positions (x, y):")
for i, pos in enumerate(positions, 1):
    print(f"  Stimulus {i}: ({pos[0]:.2f}, {pos[1]:.2f})")
```

## Example 4: Generate Frame Pattern

Create ON/OFF pattern for SSVEP:

```python
from src import generate_frame_pattern

refresh_rate = 60.0
frames_per_cycle = 4  # 15 Hz
on_frames = 2
duration_s = 1.0

pattern = generate_frame_pattern(
    frames_per_cycle,
    on_frames
)

print(f"Pattern for first {min(20, len(pattern))} frames:")
print(pattern[:20])
print(f"ON frames: {sum(pattern)}")
print(f"OFF frames: {len(pattern) - sum(pattern)}")

# Output:
# Pattern for first 20 frames:
# [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
# Total frames: 60
# ON frames: 30
# OFF frames: 30
```

## Example 5: Generate m-Sequences

Create c-VEP patterns:

```python
from src import calculate_m_sequences
import matplotlib.pyplot as plt

# Generate m-sequences for 4 stimuli
patterns = calculate_m_sequences(
    n_stim=4,
    nbits=6,  # 2^6 - 1 = 63 frames
    shift_step=4
)

print(f"Generated {len(patterns)} patterns")
print(f"Pattern length: {len(patterns[0])}")

# Show first 20 values of each pattern
print("\nFirst 20 values:")
for i, pattern in enumerate(patterns):
    print(f"Stimulus {i}: {pattern[:20].tolist()}")

# Visualize patterns
fig, axes = plt.subplots(len(patterns), 1, figsize=(12, 6))
for i, (ax, pattern) in enumerate(zip(axes, patterns)):
    ax.plot(pattern, drawstyle='steps-post', linewidth=2)
    ax.set_ylabel(f'Stim {i}')
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True, alpha=0.3)
    if i == len(patterns) - 1:
        ax.set_xlabel('Frame')

plt.suptitle('c-VEP m-Sequence Patterns')
plt.tight_layout()
plt.show()
```

## Example 6: Build Custom SSVEP Experiment

Create experiment from scratch using low-level functions:

```python
from src import (
    calculate_frequencies,
    calculate_cycle_params,
    generate_positions,
    generate_frame_pattern
)
from psychopy import visual, core

# Configuration
REFRESH_RATE = 60.0
MIN_FRAMES = 3
N_STIM = 4
DURATION_S = 10.0
DUTY_CYCLE = 0.5

# Calculate frequencies
frequencies = calculate_frequencies(REFRESH_RATE, MIN_FRAMES, N_STIM)
print(f"Frequencies: {[f'{f:.2f}' for f in frequencies]}")

# Calculate positions
positions = generate_positions(N_STIM)

# Create window
win = visual.Window(
    fullscr=True,
    units="norm",
    color=[0, 0, 0],
    waitBlanking=True
)

# Create stimuli and patterns
stimuli = []
patterns = []
total_frames = int(REFRESH_RATE * DURATION_S)

for freq, pos in zip(frequencies, positions):
    # Calculate cycle parameters
    frames_per_cycle, on_frames = calculate_cycle_params(
        REFRESH_RATE, freq, DUTY_CYCLE
    )

    # Create stimulus
    stim = visual.Rect(
        win,
        width=0.3,
        height=0.3,
        fillColor='white',
        pos=pos
    )
    stimuli.append(stim)

    # Generate pattern (one cycle only)
    pattern = generate_frame_pattern(frames_per_cycle, on_frames)
    patterns.append(pattern)

    print(f"Freq {freq:.2f} Hz: {frames_per_cycle} frames/cycle "
          f"({on_frames} ON, {frames_per_cycle - on_frames} OFF)")

# Run experiment
print("Starting experiment...")
win.recordFrameIntervals = True

for frameN in range(total_frames):
    for stim, pattern in zip(stimuli, patterns):
        stim.opacity = 1.0 if pattern[frameN % len(pattern)] == 1 else 0.0
        stim.draw()
    win.flip()

win.recordFrameIntervals = False

print(f"\nExperiment complete!")

win.close()
core.quit()
```

## Next Steps

- See [API Reference](api-core.md) for detailed function documentation
- Review [User Guide](user-guide.md) for high-level usage
