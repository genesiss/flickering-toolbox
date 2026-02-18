"""
Configuration module for flickering experiments.
"""

class ExperimentConfig:
    """Base configuration for all flickering experiments."""
    
    # Display settings
    FULLSCREEN = True           # Run in fullscreen mode (recommended)
    SCREEN_ID = 0              # Screen ID for multi-monitor setups (0 = primary)
    SCREEN_SIZE = [1920, 1080] # Window size when not fullscreen. Ignored if FULLSCREEN=True.
    
    # Timing settings
    REFRESH_RATE = 60.0        # Monitor refresh rate in Hz - MUST match actual display refresh rate!
    DURATION_S = 5.0           # Total experiment duration in seconds
    
    # Stimulus settings
    N_STIM = 9                 # Number of flickering stimuli
    STIM_SIZE = 0.3            # Stimulus size in normalized coordinates (0-1)
    STIM_COLOR = 'white'       # Stimulus color when ON
    BACKGROUND_COLOR = [0,0,0] # Background color (RGB, values -1 to 1 or color name)
    
    # Custom stimuli
    # Set these to use own visual stimuli instead of default rectangles
    CUSTOM_STIM_ON = None      # Custom stimulus for ON state
    CUSTOM_STIM_OFF = None     # Custom stimulus for OFF state
    # Should be callable: function(win, pos, size, index) -> visual object
    # The callable receives:
    #   win: PsychoPy window
    #   pos: (x, y) position tuple
    #   size: stimulus size (float)
    #   index: stimulus index (0 to N_STIM-1)
    # Use the index parameter to differentiate stimuli at different positions
    # If None, uses default rectangle with STIM_COLOR/opacity
    
    # Label settings
    SHOW_LABELS = True         # Display frequency/ID labels below stimuli
    LABEL_HEIGHT = 0.05        # Label text height
    LABEL_COLOR = 'black'      # Label text color
    LABEL_OFFSET = 0.05        # Distance below stimulus
    
    # Callback settings
    FLIP_CALLBACK = None       # Callback function called after each window flip
                               # Should be callable: function(frame_number, timestamp) -> None
                               # Useful for sending triggers to EEG/MEG equipment
    
    # Logging settings
    LOG_FILE = "flicker_log.log"
    LOG_LEVEL = "INFO"         # Logging detail level: INFO, WARNING, ERROR


class SSVEPConfig(ExperimentConfig):
    """Configuration specific to SSVEP (frequency-based) experiments."""

    MIN_FRAMES_PER_CYCLE = 3   # Minimum frames per flicker cycle (controls max frequency)
                               # At 60Hz: MIN_FRAMES=3 → max frequency is 60Hz/3=20Hz, MIN_FRAMES=4 → max frequency is 60Hz/4=15Hz
    DUTY_CYCLE = 0.5           # Ratio of ON time per cycle (0.5 = 50% ON, 50% OFF)
    CUSTOM_FREQUENCIES = None  # List of custom frequencies in Hz (e.g., [10.0, 12.0, 15.0])
                               # If provided, these will be used instead of auto-calculated frequencies
                               # Must be achievable with the given REFRESH_RATE (should divide evenly)
                               # Length determines N_STIM (overrides N_STIM setting)

class CVEPConfig(ExperimentConfig):
    """Configuration specific to c-VEP (code-modulated) experiments."""
    
    # m-sequence generation parameters
    NBITS = 6                  # Number of bits (sequence length = 2^NBITS - 1)
                               # NBITS=6 → 63 frames per sequence
    SHIFT_STEP = 4             # Circular shift between stimuli