# Configuration Reference

This page describes configuration parameters available in Flickering Toolbox.

## Configuration Classes

### ExperimentConfig (Base)

Base class containing all common parameters:

```python
from src import ExperimentConfig

config = ExperimentConfig()
```

### SSVEPConfig

SSVEP-specific configuration (inherits from `ExperimentConfig`):

```python
from src import SSVEPConfig

config = SSVEPConfig()
```

### CVEPConfig

c-VEP-specific configuration (adds m-sequence parameters):

```python
from src import CVEPConfig

config = CVEPConfig()
```

## Display Settings

### FULLSCREEN
- **Type**: `bool`
- **Default**: `True`
- **Description**: Run in fullscreen mode
- **Recommendation**: Always use `True` for experiments

```python
config.FULLSCREEN = True
```

### SCREEN_ID
- **Type**: `int`
- **Default**: `0`
- **Description**: Monitor ID for multi-monitor setups
- **Values**: `0` = primary, `1` = secondary, etc.

```python
config.SCREEN_ID = 1  # Use secondary monitor
```

### SCREEN_SIZE
- **Type**: `list[int, int]`
- **Default**: `[1920, 1080]`
- **Description**: Window size when not fullscreen
- **Format**: `[width, height]` in pixels

```python
config.SCREEN_SIZE = [1280, 720]
```

### BACKGROUND_COLOR
- **Type**: `str` or `list[float, float, float]`
- **Default**: `[0, 0, 0]` (black)
- **Description**: Background color of experiment window
- **Formats**: 
  - RGB values from -1 to 1: `[0, 0, 0]` (black), `[1, 1, 1]` (white)
  - Color names: `'black'`, `'white'`, `'gray'`

```python
config.BACKGROUND_COLOR = [0.2, 0.2, 0.2]  # Dark gray
config.BACKGROUND_COLOR = 'gray'
```

## Callback Settings

### FLIP_CALLBACK
- **Type**: `callable` or `None`
- **Default**: `None`
- **Description**: Function called after each window flip
- **Signature**: `function(frame_number: int, timestamp: float) -> None`
- **Parameters**:
  - `frame_number`: Current frame index (0, 1, 2, ...)
  - `timestamp`: Exact flip time from PsychoPy
- **Use cases**:
  - Sending triggers via parallel port
  - Logging frame timings
  - Synchronizing with external equipment

```python
# Example 1: Simple logging
def log_frame(frame_num, timestamp):
    print(f"Frame {frame_num} at {timestamp:.4f}s")

config.FLIP_CALLBACK = log_frame
```

**Important**: Callbacks should execute quickly (< 1ms) to avoid frame drops. Use non-blocking operations only.

## Timing Settings

### REFRESH_RATE
- **Type**: `float`
- **Default**: `60.0`
- **Description**: Monitor refresh rate in Hz

```python
config.REFRESH_RATE = 120.0  # For 120Hz monitor
```

!!! danger "Critical Parameter"
    Incorrect `REFRESH_RATE` will cause timing errors and invalidate results!

### DURATION_S
- **Type**: `float`
- **Default**: `5.0`
- **Description**: Total experiment duration in seconds
- **Range**: Any positive value

```python
config.DURATION_S = 15.0  # 15-second experiment
```

## Stimulus Settings

### N_STIM
- **Type**: `int`
- **Default**: `9`
- **Description**: Number of flickering stimuli
- **Layout**: Automatically arranged in grid (e.g., 4 = 2×2, 9 = 3×3, 6 = 3×2)
- **Maximum**: `REFRESH_RATE - MIN_FRAMES_PER_CYCLE + 1`

```python
config.N_STIM = 6
```

!!! tip "Maximum Stimuli"
    ```python
    max_stimuli = config.REFRESH_RATE - config.MIN_FRAMES_PER_CYCLE + 1
    ```
    
    At 60Hz with `MIN_FRAMES=3`: max 58 stimuli
    
    At 120Hz with `MIN_FRAMES=3`: max 118 stimuli

### STIM_SIZE
- **Type**: `float`
- **Default**: `0.3`
- **Description**: Stimulus size in normalized coordinates
- **Range**: `0.0` to `1.0`

```python
config.STIM_SIZE = 0.4
```

### STIM_COLOR
- **Type**: `str`
- **Default**: `'white'`
- **Description**: Color when stimulus is ON
- **Options**: Color names (`'white'`, `'red'`, `'blue'`) or RGB values

```python
config.STIM_COLOR = 'yellow'
config.STIM_COLOR = [1.0, 0.5, 0.0]  # Orange
```

## Custom Stimuli

### CUSTOM_STIM_ON
- **Type**: `callable` or `None`
- **Default**: `None`
- **Description**: Custom visual stimulus for ON state
- **Signature**: `function(win, pos, size, index) -> visual object`

The callable receives:  
- `win`: PsychoPy window object   
- `pos`: `(x, y)` position tuple (normalized coordinates)   
- `size`: Stimulus size as float    
- `index`: Stimulus index (0 to N_STIM-1)   

```python
from psychopy import visual

def create_gabor_on(win, pos, size, index):
    return visual.GratingStim(
        win, 
        tex='sin',
        mask='gauss',
        pos=pos,
        size=size,
        sf=5,
        ori=index * 45  # Different orientations per stimulus
    )

config.CUSTOM_STIM_ON = create_gabor_on
```

!!! tip "Using Index Parameter"
    Use the `index` parameter to differentiate stimuli:
    ```python
    def create_letter(win, pos, size, index):
        letters = ['A', 'B', 'C', 'D']
        return visual.TextStim(
            win, 
            text=letters[index % len(letters)],
            pos=pos,
            height=size
        )
    ```

### CUSTOM_STIM_OFF
- **Type**: `callable` or `None`
- **Default**: `None`
- **Description**: Custom visual stimulus for OFF state
- **Signature**: Same as `CUSTOM_STIM_ON`

```python
def create_gabor_off(win, pos, size, index):
    return visual.GratingStim(
        win,
        tex='sin',
        mask='gauss',
        pos=pos,
        size=size,
        sf=5,
        contrast=0.2,  # Low contrast for OFF state
        ori=index * 45
    )

config.CUSTOM_STIM_OFF = create_gabor_off
```

!!! warning "Using Custom Stimuli"
    - When using custom stimuli, `STIM_COLOR` is ignored
    - Both `CUSTOM_STIM_ON` and `CUSTOM_STIM_OFF` should return PsychoPy visual objects
    - If only one is set, the other state will use default behavior

## Label Settings

### SHOW_LABELS
- **Type**: `bool`
- **Default**: `True`
- **Description**: Display frequency/ID labels below stimuli
- **SSVEP**: Shows frequency (e.g., "15.00 Hz")
- **c-VEP**: Shows stimulus index (e.g., "0", "1", "2")

```python
config.SHOW_LABELS = False  # Hide labels
```

### LABEL_HEIGHT
- **Type**: `float`
- **Default**: `0.05`
- **Description**: Label text height in normalized coordinates

```python
config.LABEL_HEIGHT = 0.08  # Larger text
```

### LABEL_COLOR
- **Type**: `str`
- **Default**: `'black'`
- **Description**: Label text color

```python
config.LABEL_COLOR = 'white'
```

### LABEL_OFFSET
- **Type**: `float`
- **Default**: `0.05`
- **Description**: Distance below stimulus to place label

```python
config.LABEL_OFFSET = 0.1  # Further from stimulus
```

## Logging Settings

### LOG_FILE
- **Type**: `str`
- **Default**: `"flicker_log.log"`
- **Description**: File path for experiment logs

```python
config.LOG_FILE = "my_experiment.log"
config.LOG_FILE = "/path/to/logs/exp_001.txt"
```

### LOG_LEVEL
- **Type**: `str`
- **Default**: `"INFO"`
- **Description**: Logging detail level
- **Options**: `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`

```python
config.LOG_LEVEL = "DEBUG"  # Verbose logging
```

## SSVEP Specific Settings

### MIN_FRAMES_PER_CYCLE
- **Type**: `int`
- **Default**: `3`
- **Description**: Minimum frames per flicker cycle (controls maximum frequency)
- **Effect**: At 60Hz, `MIN_FRAMES=3` → max 20Hz, `MIN_FRAMES=4` → max 15Hz

```python
config.MIN_FRAMES_PER_CYCLE = 4  # Lower maximum frequency
```

**Frequency calculation:**
```
max_frequency = REFRESH_RATE / MIN_FRAMES_PER_CYCLE
```

### CUSTOM_FREQUENCIES
- **Type**: `list[float]` or `None`
- **Default**: `None`
- **Description**: Specify custom frequencies instead of auto-calculation
- **Note**: When set, overrides both `N_STIM` and `MIN_FRAMES_PER_CYCLE`

```python
config.CUSTOM_FREQUENCIES = [10.0, 12.0, 15.0, 20.0]
# N_STIM automatically becomes 4 (length of list)
```

!!! tip "Frequencies"
    For stable timing, use frequencies that divide `REFRESH_RATE` evenly:
    
    At 60Hz: 10, 12, 15, 20, 30 Hz
    
    At 120Hz: 10, 12, 15, 20, 24, 30, 40 Hz
    
!!! warning
    Non-integer divisors (e.g., 13Hz at 60Hz) may cause timing drift.


### DUTY_CYCLE
- **Type**: `float`
- **Default**: `0.5`
- **Description**: Ratio of ON time per cycle
- **Range**: `0.0` to `1.0`
- **Examples**: 
  - `0.5` = 50% ON, 50% OFF
  - `0.25` = 25% ON, 75% OFF
  - `0.75` = 75% ON, 25% OFF

```python
config.DUTY_CYCLE = 0.25
```    

## c-VEP Specific Settings

### NBITS
- **Type**: `int`
- **Default**: `6`
- **Description**: Number of bits for m-sequence generation
- **Sequence length**: `2^NBITS - 1`
- **Examples**: 
  - `NBITS=6` → 63 frames
  - `NBITS=7` → 127 frames
  - `NBITS=5` → 31 frames

```python
config.NBITS = 7  # Longer sequence
```

### SHIFT_STEP
- **Type**: `int`
- **Default**: `4`
- **Description**: Circular shift between stimuli patterns
- **Formula**: Stimulus k uses shift `k * SHIFT_STEP`

```python
config.SHIFT_STEP = 8  # Larger separation between patterns
```

## Configuration Examples

### High-Frequency SSVEP (120Hz Monitor)

```python
from src import SSVEPConfig

config = SSVEPConfig()
config.REFRESH_RATE = 120.0
config.MIN_FRAMES_PER_CYCLE = 3  # Max 40Hz
config.N_STIM = 8
config.DURATION_S = 20.0
config.FULLSCREEN = True
```

### Large Stimuli

```python
from src import SSVEPConfig

config = SSVEPConfig()
config.N_STIM = 4
config.STIM_SIZE = 0.5  # Large stimuli
config.STIM_COLOR = 'white'
config.BACKGROUND_COLOR = 'black'
config.DUTY_CYCLE = 0.5
config.DURATION_S = 30.0
```

### c-VEP with Long Sequences

```python
from src import CVEPConfig

config = CVEPConfig()
config.N_STIM = 16
config.NBITS = 7  # 127-frame sequence
config.SHIFT_STEP = 8
config.DURATION_S = 60.0
config.SHOW_LABELS = False
```

## Validation

Configuration values are validated when experiments run. Common errors:

```python
# Too many stimuli
config.N_STIM = 100  # Will raise AssertionError

# Invalid refresh rate
config.REFRESH_RATE = 0  # Will raise AssertionError

# Valid configuration
config.N_STIM = 9
config.REFRESH_RATE = 60.0
```

## Next Steps

- See [User Guide](user-guide.md) for usage patterns
- Check [Examples](examples.md) for complete code samples