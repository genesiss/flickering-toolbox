# Core computational functions
from .flicker_core import (
    calculate_frequencies,
    calculate_cycle_params,
    generate_positions,
    generate_frame_pattern,
    calculate_m_sequences
)

# Configuration classes
from .config import (
    ExperimentConfig,
    SSVEPConfig,
    CVEPConfig
)

# High-level experiment classes
from .experiment import (
    FlickerExperiment,
    SSVEPExperiment,
    CVEPExperiment
)

__all__ = [
    # Core functions
    'calculate_frequencies',
    'calculate_cycle_params',
    'generate_positions',
    'generate_frame_pattern',
    'calculate_m_sequences',
    # Configuration
    'ExperimentConfig',
    'SSVEPConfig',
    'CVEPConfig',
    # Experiment classes
    'FlickerExperiment',
    'SSVEPExperiment',
    'CVEPExperiment',
]

__version__ = '1.0.0'
