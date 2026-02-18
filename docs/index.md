# Flickering Toolbox

Flickering Toolbox is a library that provides easy-to-use tools for generating visual flickering stimuli, specifically designed for SSVEP (Steady-State Visual Evoked Potentials) and c-VEP (code-modulated Visual Evoked Potential) experiments.

## What is Flickering Toolbox?

Flickering Toolbox is a Python library built on top of PsychoPy that enables creation of flickering visual stimuli for brain-computer interface (BCI) and neuroscience research. 

### Key Features

**Easy to Use**: Simple API designed for students without programming background    
**Frame-Perfect Timing**: All flickering synchronized to monitor VBlank intervals  
**Two Paradigms**: Support for both SSVEP (frequency-based) and c-VEP (pattern-based)  
**Library Design**: Import and use in your own Python scripts  
**Configurable**: Different behavior can be achieved through configuration

## Quick Example

```python
from src import SSVEPExperiment, SSVEPConfig

# Configure experiment
config = SSVEPConfig()
config.N_STIM = 4
config.DURATION_S = 10.0

# Run experiment
experiment = SSVEPExperiment(config)
report = experiment.run()

# Close experiment
experiment.close()
```

## Why Frame-Perfect Timing Matters

Unlike time-based approaches, Flickering Toolbox uses **frame-based** flickering where all frequencies are calculated as:

```
frequency = refresh_rate / integer_divisor
```

This ensures perfect alignment with your monitor's hardware refresh cycles, eliminating visual artifacts and ensuring reliable brain responses.

## Getting Started

Check out the [Installation Guide](getting-started.md) and [Quick Start Tutorial](quick-start.md)!

## Project Structure

```
flickering-toolbox/
├── src/                                          # Core library code
│   ├── flicker_core.py                           # Pure computational functions
│   ├── experiment.py                             # High-level experiment classes
│   ├── config.py                                 # Configuration system
│   └── __init__.py                               # Package exports
├── examples/                                     # Usage examples
├── tests/                                        # Unit test suite
├── docs/                                         # Documentation
├── requirements.txt                              # Python dependencies
├── mkdocs.yml                                    # Documentation config
└── README.md                                     # Main readme
```

## Support

- [User Guide](user-guide.md) - Learn how to use the library
- [API Reference](api-core.md) - Detailed function documentation
- [Examples](examples.md) - Code examples and patterns
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
