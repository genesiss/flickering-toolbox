# Flickering Toolbox

A user-friendly Python library for generating visual flickering stimuli in cognitive science research using PsychoPy.

## Features

- **SSVEP (Steady-State Visually Evoked Potentials)**: Frequency-based flickering stimuli
- **c-VEP (Code-modulated VEP)**: m-sequence based flickering stimuli
- **Easy configuration**: Simple Python API for students
- **Custom stimuli**: Support for custom visual elements

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### SSVEP Experiment

```python
from src import SSVEPExperiment, SSVEPConfig

config = SSVEPConfig()
config.N_STIM = 4
config.DURATION_S = 10.0

experiment = SSVEPExperiment(config)
report = experiment.run()
experiment.close()
```

### c-VEP Experiment

```python
from src import CVEPExperiment, CVEPConfig

config = CVEPConfig()
config.N_STIM = 4
config.DURATION_S = 10.0

experiment = CVEPExperiment(config)
report = experiment.run()
experiment.close()
```

## Documentation

Full documentation available in the `docs/` folder.

### Building the Documentation

#### Install Dependencies

```bash
pip install mkdocs mkdocs-material mkdocstrings pymdown-extensions
```

#### Serve Locally

```bash
mkdocs serve
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material Theme](https://squidfunk.github.io/mkdocs-material/)
- [Markdown Guide](https://www.markdownguide.org/)

## Examples

See the `examples/` folder for:
- Basic SSVEP and c-VEP experiments
- Custom frequency configurations
- Custom stimuli (Gabor patches, letters, images)
- EEG trigger integration

## Testing

```bash
python -m pytest tests/
```

## License

See [LICENSE](LICENSE) file for details.
