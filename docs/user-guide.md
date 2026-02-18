# User Guide: Using as a Library

This guide explains how to use Flickering Toolbox as a Python library in your own research projects.

## Import Patterns

The library provides imports from the `src` package:

```python
# Import experiment classes
from src import SSVEPExperiment, CVEPExperiment

# Import configuration classes
from src import SSVEPConfig, CVEPConfig, ExperimentConfig

# Import core functions (for low-level usage)
from src import (
    calculate_frequencies,
    calculate_cycle_params,
    generate_positions,
    generate_frame_pattern,
    calculate_m_sequences
)
```

## High-Level API (Recommended)

The easiest way to use the library is through the experiment classes.

### SSVEP Experiment

```python
from src import SSVEPExperiment, SSVEPConfig

# Create and configure
config = SSVEPConfig()
config.N_STIM = 6
config.DURATION_S = 15.0
config.REFRESH_RATE = 120.0  # High refresh rate monitor

# Run experiment
experiment = SSVEPExperiment(config)
report = experiment.run()

experiment.close()
```

### c-VEP Experiment

```python
from src import CVEPExperiment, CVEPConfig

# Create and configure
config = CVEPConfig()
config.N_STIM = 9
config.DURATION_S = 20.0
config.NBITS = 6  # 63-frame m-sequence
config.SHIFT_STEP = 4

# Run experiment
experiment = CVEPExperiment(config)
report = experiment.run()

experiment.close()
```

## Configuration

### Direct Configuration

```python
from src import SSVEPExperiment, SSVEPConfig

config = SSVEPConfig()
config.N_STIM = 4
config.DURATION_S = 10.0
config.FULLSCREEN = True

experiment = SSVEPExperiment(config)
```

### Custom Configuration Class

```python
from src import SSVEPConfig, SSVEPExperiment

class MyExperimentConfig(SSVEPConfig):
    """Configuration for my research project."""
    REFRESH_RATE = 120.0
    MIN_FRAMES_PER_CYCLE = 4
    N_STIM = 8
    DURATION_S = 30.0
    STIM_SIZE = 0.35
    STIM_COLOR = 'yellow'
    BACKGROUND_COLOR = [0.2, 0.2, 0.2]
    
# Use it
config = MyExperimentConfig()
experiment = SSVEPExperiment(config)
```

## Advanced Usage

### Multiple Experiments in Sequence

This usage pattern can be useful if you want to try out different experiment configurations in one go.

```python
from src import SSVEPExperiment, SSVEPConfig
from psychopy import core, visual, event

def create_instruction_window():
    """Create and return a window for displaying instructions."""
    return visual.Window(
        size=[800, 600],
        units="norm",
        fullscr=True,
        color=[0, 0, 0]
    )

# Define configurations for multiple experiments
configs = []

# Experiment 1: 4 stimuli
config1 = SSVEPConfig()
config1.N_STIM = 4
config1.DURATION_S = 3.0
configs.append(("4 stimuli", config1))

# Experiment 2: 6 stimuli
config2 = SSVEPConfig()
config2.N_STIM = 6
config2.DURATION_S = 3.0
configs.append(("6 stimuli", config2))

# Experiment 3: 9 stimuli
config3 = SSVEPConfig()
config3.N_STIM = 9
config3.DURATION_S = 3.0
configs.append(("9 stimuli", config3))

# Run all experiments
print(f"Running {len(configs)} experiments...\n")

# Create a window for instructions
instruction_win = create_instruction_window()

for i, (description, config) in enumerate(configs, 1):
    print(f"===== Experiment {i}/{len(configs)}: {description} =====")
    
    # Show instruction screen
    instruction_text = visual.TextStim(
        instruction_win,
        text=f"Starting Experiment {i}/{len(configs)}\n\n{description}\n\nPress SPACE to begin",
        height=0.1,
        color='white'
    )
    instruction_text.draw()
    instruction_win.flip()
    
    event.waitKeys(keyList=['space'])
    
    # Close instruction window before starting experiment
    instruction_win.close()
    
    # Run the experiment
    experiment = SSVEPExperiment(config)
    report = experiment.run()
    
    # Close experiment window
    if experiment.win:
        experiment.win.close()
    
    # Recreate instruction window for next iteration (if not last experiment)
    if i < len(configs):
        instruction_win = create_instruction_window()

core.quit()

print("All experiments completed!")
```

## Next Steps

- See [Configuration Guide](configuration.md) for all available parameters
- Check [Examples](examples.md) for more code patterns
- Review [API Reference](api-core.md) for detailed documentation
