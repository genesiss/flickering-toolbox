# Examples: Basic Usage

Examples for common use cases.

## Example 1: Minimal SSVEP Experiment

The simplest possible experiment:

```python
from src import SSVEPExperiment, SSVEPConfig

config = SSVEPConfig()
experiment = SSVEPExperiment(config)
experiment.run()
experiment.close()
```

This uses all default settings (9 stimuli, 5 seconds, 60Hz).

## Example 2: Custom Number of Stimuli

4 stimuli for 10 seconds:

```python
from src import SSVEPExperiment, SSVEPConfig

config = SSVEPConfig()
config.N_STIM = 4
config.DURATION_S = 10.0

experiment = SSVEPExperiment(config)
report = experiment.run()
experiment.close()
```

## Example 3: c-VEP Experiment

Using code-modulated patterns:

```python
from src import CVEPExperiment, CVEPConfig

config = CVEPConfig()
config.N_STIM = 9
config.DURATION_S = 15.0
config.NBITS = 6  # 63-frame m-sequence

experiment = CVEPExperiment(config)
report = experiment.run()
experiment.close()
```

## Example 4: High Refresh Rate Monitor

For 120Hz displays:

```python
from src import SSVEPExperiment, SSVEPConfig

config = SSVEPConfig()
config.REFRESH_RATE = 120.0
config.MIN_FRAMES_PER_CYCLE = 3  # Max frequency: 40Hz
config.N_STIM = 8
config.DURATION_S = 20.0

experiment = SSVEPExperiment(config)
report = experiment.run()
experiment.close()
```

## Example 5: Large Stimuli
```python
from src import SSVEPExperiment, SSVEPConfig

config = SSVEPConfig()
config.N_STIM = 4
config.STIM_SIZE = 0.5  # Large stimuli
config.STIM_COLOR = 'white'
config.BACKGROUND_COLOR = 'black'
config.DURATION_S = 30.0
config.SHOW_LABELS = False  # Clean display

experiment = SSVEPExperiment(config)
report = experiment.run()
experiment.close()
```

## Example 6: Custom Colors

Experiment with different color schemes:

```python
from src import SSVEPExperiment, SSVEPConfig

# Dark mode
config = SSVEPConfig()
config.STIM_COLOR = 'white'
config.BACKGROUND_COLOR = [0, 0, 0]
config.LABEL_COLOR = 'white'

# Light mode
# config.STIM_COLOR = 'black'
# config.BACKGROUND_COLOR = [1, 1, 1]
# config.LABEL_COLOR = 'black'

# Custom colors (RGB -1 to 1)
# config.STIM_COLOR = [1.0, 0.5, 0.0]  # Orange
# config.BACKGROUND_COLOR = [0.2, 0.2, 0.3]  # Blue-gray

experiment = SSVEPExperiment(config)
report = experiment.run()
experiment.close()
```

## Example 7: Window flip callback

```python
from src import SSVEPExperiment, SSVEPConfig
from psychopy import logging

def log_flip_times(frame_num, timestamp):
    """Log each flip time to console."""
    logging.info(f"Frame {frame_num}: flip at {timestamp:.4f}s")


config = SSVEPConfig()
config.N_STIM = 9               
config.DURATION_S = 10.0        
config.REFRESH_RATE = 60.0
config.FLIP_CALLBACK = log_flip_times  # Set the flip callback

experiment = SSVEPExperiment(config)
report = experiment.run()
experiment.close()
```

## Example 8: Copying Example Files

You can also start by copying the provided examples. Following examples are available:

### Simple SSVEP experiment

```bash
# Copy example
cp examples/run_flicker_experiment_ssvep.py my_experiment.py

# Edit and run
python my_experiment.py
```

### c-VEP experiment

```bash
# Copy example
cp examples/run_flicker_experiment_cvep.py my_cvep_experiment.py

# Edit and run
python my_cvep_experiment.py
```

### SSVEP with custom frequencies

```bash
# Copy example
cp examples/run_flicker_experiment_ssvep_custom_freqs.py my_custom_freqs.py

# Edit and run
python my_custom_freqs.py
```

### Custom stimuli examples

```bash
# Gabor patches
cp examples/custom_stimuli_gabor.py my_gabor_experiment.py
python my_gabor_experiment.py

# Letter stimuli
cp examples/custom_stimuli_letters.py my_letters_experiment.py
python my_letters_experiment.py

# Mixed stimuli (images + text)
cp examples/custom_stimuli_mixed.py my_mixed_experiment.py
python my_mixed_experiment.py
```

### Frame flip trigger callback example

```bash
# Copy EEG callback example
cp examples/eeg_trigger_callback.py my_eeg_experiment.py
python my_eeg_experiment.py
```

## Next Steps

- Check [Low-Level API Examples](examples-lowlevel.md) for manual control
- Read [User Guide](user-guide.md) for detailed explanations
- Review [Configuration Reference](configuration.md) for all parameters
