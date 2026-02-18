# Quick Start

This guide will help you run your first flickering experiment in minutes!

## Running Example Experiments

### SSVEP Experiment

Run a simple frequency-based flickering experiment:

```bash
python -m examples.run_flicker_experiment_ssvep
```

This will:

- Display 9 flickering stimuli in a 3×3 grid    
- Each stimulus flickers at a different frequency (automatically calculated)   
- Run for 10 seconds     
- Display results including stability metrics in the console

### c-VEP Experiment

Run a code-modulated experiment:

```bash
python -m examples.run_flicker_experiment_cvep
```

This uses m-sequences instead of fixed frequencies.

## Your First Custom Experiment

Create a new file `my_experiment.py`:

```python
from src import SSVEPExperiment, SSVEPConfig

# Create configuration
config = SSVEPConfig()
config.N_STIM = 4           # 4 stimuli
config.DURATION_S = 10.0    # 10 seconds
config.REFRESH_RATE = 60.0  # Match your monitor!

# Run experiment
experiment = SSVEPExperiment(config)
report = experiment.run()

experiment.close()
```

Run it:

```bash
python my_experiment.py
```

## Understanding the Output

When the experiment completes, you'll see:

```
31.3813 	INFO 	===== Report =====
31.3813 	INFO 	Dropped frames: 2
31.3813 	INFO 	Total frames recorded: 699
31.3813 	INFO 	Average frame interval: 16.662 ms (expected based on refresh rate 16.667 ms)
31.3813 	INFO 	Stability percent: 99.71 %
31.3813 	INFO 	Experiment ended.
============================================================
Logs are written to 'flicker_log.log' too.
```

### Key Metrics

- **Dropped frames**: Should be 0 (or very close)
- **Stability**: Should be close to 100%
- **Mean interval**: Should match expected (e.g., 16.67ms for 60Hz)

!!! success "Good Results"
    - Dropped frames: 0
    - Stability: > 99%
    - Mean interval within 0.5ms of expected

!!! warning "Concerning Results"
    - Dropped frames: > 1% of total
    - Stability: < 95%
    - Mean interval differs by > 1ms

    → See [Troubleshooting](troubleshooting.md)

## Customizing Your Experiment

Edit the configuration to suit your needs:

```python
config = SSVEPConfig()

# Display settings
config.FULLSCREEN = True
config.SCREEN_ID = 0  # Primary monitor

# Timing
config.REFRESH_RATE = 60.0
config.DURATION_S = 15.0
config.MIN_FRAMES_PER_CYCLE = 3

# Stimuli
config.N_STIM = 6
config.STIM_SIZE = 0.4  # Larger stimuli
config.STIM_COLOR = 'white'
config.BACKGROUND_COLOR = [1, 0, 0]  # Pink

# Visual feedback
config.SHOW_LABELS = True  # Display frequencies
```

## Understanding Frequencies

At 60Hz with `MIN_FRAMES_PER_CYCLE = 3`:

```python
frequencies = calculate_frequencies(60.0, 3, 4)
print(frequencies)
# Output: [20.0, 15.0, 12.0, 10.0]
```

These correspond to:

- 20Hz: 3 frames/cycle (2 ON, 1 OFF with duty_cycle=0.5)    
- 15Hz: 4 frames/cycle (2 ON, 2 OFF)    
- 12Hz: 5 frames/cycle  (2 ON, 3 OFF)
- 10Hz: 6 frames/cycle  (3 ON, 3 OFF)

Check the logs during experiment. Frequency data for each stimuli will be present in log. Example:

```
26.7983         INFO    Stim 3: 12.00 Hz → 5 frames/cycle (2 ON, 3 OFF)
```

## Checking the Logs

Open `flicker_log.log` to see detailed information:

```
===== Starting SSVEP Flickering Experiment =====
25.0044 	INFO 	===== Starting Flickering Experiment =====
25.0044 	INFO 	Configuration: N_STIM=6, DURATION=15.0s, REFRESH_RATE=60.0Hz, MIN_FRAMES=3
26.7527 	INFO 	Auto-calculated frequencies (Hz): [20.0, 15.0, 12.0, 10.0, 8.571, 7.5]
26.7898 	INFO 	Stim 1: 20.00 Hz → 3 frames/cycle (2 ON, 1 OFF)
26.7955 	INFO 	Stim 2: 15.00 Hz → 4 frames/cycle (2 ON, 2 OFF)
...
34.3312 	INFO 	===== Report =====
34.3312 	INFO 	Dropped frames: 2
34.3312 	INFO 	Total frames recorded: 999
34.3313 	INFO 	Average frame interval: 8.409 ms (expected based on refresh rate 16.667 ms)
34.3313 	INFO 	SD of frame intervals: 3.992 ms
34.3313 	INFO 	Stability percent: 99.80 %
34.3313 	INFO 	Experiment ended.
```

## Next Steps

- **Learn more**: Read the [User Guide](user-guide.md) for detailed usage patterns
- **Explore examples**: Check [Examples](examples.md) for more code samples
- **API reference**: See [API Documentation](api-core.md) for all functions
