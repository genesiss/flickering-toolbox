"""
Experiment wrapper classes.
"""
from abc import ABC, abstractmethod

from psychopy import visual, core, logging
from .flicker_core import (
    calculate_frequencies, 
    calculate_cycle_params, 
    generate_positions, 
    generate_frame_pattern,
    calculate_m_sequences
)
from .config import SSVEPConfig, CVEPConfig


class FlickerExperiment(ABC):
    """Abstract base class for flickering experiments."""
    
    def __init__(self, config):
        """
        Initialize experiment with configuration.
        
        Args:
            config: ExperimentConfig instance (SSVEPConfig or CVEPConfig)
        """
        self.config = config
        self.win = None
        self.stimuli = []
        self.labels = []
        self.patterns = []
        self.custom_stim_on = []   # Store custom ON stimuli if provided
        self.custom_stim_off = []  # Store custom OFF stimuli if provided
        
    def setup_logging(self):
        """Configure logging based on config settings."""
        log_level = getattr(logging, self.config.LOG_LEVEL.upper())
        logging.console.setLevel(log_level)
        self.logfile = logging.LogFile(self.config.LOG_FILE, level=log_level, filemode='w')
        
    def create_window(self):
        """Create PsychoPy window with configured settings."""
        self.win = visual.Window(
            screen=self.config.SCREEN_ID,
            size=self.config.SCREEN_SIZE,
            units="norm",
            fullscr=self.config.FULLSCREEN,
            color=self.config.BACKGROUND_COLOR,
            allowGUI=False,
            waitBlanking=True
        )
        return self.win
    
    def close(self):
        """Close window and quit PsychoPy."""
        if self.win:
            self.win.close()
        core.quit()
        
    def get_report(self):
        """
        Get experiment statistics report.
        
        Returns:
            dict: Statistics including dropped frames, frame intervals, etc.
        """
        if not self.win or not self.win.frameIntervals:
            return {"error": "No frame data available"}
        
        intervals = self.win.frameIntervals
        mean_int = sum(intervals) / len(intervals)
        sd_int = (sum((i - mean_int)**2 for i in intervals) / len(intervals))**0.5
        stable_percent = 100 * (1 - self.win.nDroppedFrames / len(intervals))
        
        return {
            "dropped_frames": self.win.nDroppedFrames,
            "total_frames": len(intervals),
            "mean_interval_ms": mean_int * 1000,
            "expected_interval_ms": 1000 / self.config.REFRESH_RATE,
            "sd_interval_ms": sd_int * 1000,
            "stability_percent": stable_percent
        }
    
    def log_report(self):
        """Log experiment statistics to logging system."""
        report = self.get_report()
        logging.info("===== Report =====")
        logging.info(f"Dropped frames: {report.get('dropped_frames', 'N/A')}")
        if 'total_frames' in report:
            logging.info(f"Total frames recorded: {report['total_frames']}")
            logging.info(f"Average frame interval: {report['mean_interval_ms']:.3f} ms "
                        f"(expected based on refresh rate {report['expected_interval_ms']:.3f} ms)")
            logging.info(f"SD of frame intervals: {report['sd_interval_ms']:.3f} ms")
            logging.info(f"Stability percent: {report['stability_percent']:.2f} %")
    
    def _create_custom_stimulus(self, custom_config, position, size, index):
        """Helper to create a custom stimulus.
        
        Args:
            custom_config: Callable function(win, pos, size, index) -> visual object (or None)
            position: (x, y) position tuple
            size: stimulus size
            index: stimulus index
            
        Returns:
            PsychoPy visual stimulus or None
        """
        if custom_config is None:
            return None
        
        if callable(custom_config):
            return custom_config(self.win, position, size, index)
        else:
            return None
    
    def _create_default_stimulus(self, position):
        """Helper to create default rectangle stimulus.
        
        Args:
            position: (x, y) position tuple
            
        Returns:
            PsychoPy Rect stimulus
        """
        return visual.Rect(
            self.win,
            width=self.config.STIM_SIZE,
            height=self.config.STIM_SIZE,
            fillColor=self.config.STIM_COLOR,
            pos=position
        )
    
    def _create_label(self, text, position):
        """Helper to create stimulus label.
        
        Args:
            text: Label text to display
            position: (x, y) position of the stimulus
            
        Returns:
            PsychoPy TextStim or None if labels disabled
        """
        if not self.config.SHOW_LABELS:
            return None
        
        return visual.TextStim(
            self.win,
            text=text,
            pos=(position[0], position[1] - self.config.STIM_SIZE/2 - self.config.LABEL_OFFSET),
            height=self.config.LABEL_HEIGHT,
            color=self.config.LABEL_COLOR
        )
    
    def _create_stimulus_at_position(self, position, index, label_text):
        """Helper to create stimulus (custom or default) and label at a position.
        
        Args:
            position: (x, y) position tuple
            index: stimulus index
            label_text: text for the label
        """
        use_custom = self.config.CUSTOM_STIM_ON is not None or self.config.CUSTOM_STIM_OFF is not None
        
        if use_custom:
            stim_on = self._create_custom_stimulus(self.config.CUSTOM_STIM_ON, position, self.config.STIM_SIZE, index)
            stim_off = self._create_custom_stimulus(self.config.CUSTOM_STIM_OFF, position, self.config.STIM_SIZE, index)
            self.custom_stim_on.append(stim_on)
            self.custom_stim_off.append(stim_off)
            self.stimuli.append(None)  # Placeholder
        else:
            stim = self._create_default_stimulus(position)
            self.stimuli.append(stim)
        
        # Create label
        label = self._create_label(label_text, position)
        if label:
            self.labels.append(label)
    
    @abstractmethod
    def prepare_stimuli(self):
        """Prepare all stimuli and patterns for the experiment.
        
        Must be implemented by subclasses to generate experiment-specific
        stimuli and flicker patterns.
        """
        pass
    
    def get_experiment_name(self):
        """Get experiment type name for logging. Override in subclasses."""
        return "Flickering Experiment"
    
    def get_experiment_info(self):
        """Get experiment configuration info for logging. Override in subclasses."""
        return f"N_STIM={self.config.N_STIM}, DURATION={self.config.DURATION_S}s, REFRESH_RATE={self.config.REFRESH_RATE}Hz"
    
    def run(self):
        """Run the complete flickering experiment."""
        self.setup_logging()
        logging.info(f"===== Starting {self.get_experiment_name()} =====")
        logging.info(f"Configuration: {self.get_experiment_info()}")
        
        self.create_window()
        logging.info("Window open.")
        
        self.prepare_stimuli()
        
        # Main loop
        total_frames = int(self.config.REFRESH_RATE * self.config.DURATION_S)
        logging.info(f"Starting flickering sequence (Estimated number of frames: {total_frames}).")
        
        self.win.recordFrameIntervals = True
        self.win.refreshThreshold = (1.0 / self.config.REFRESH_RATE) + 0.004
        
        use_custom = self.config.CUSTOM_STIM_ON is not None or self.config.CUSTOM_STIM_OFF is not None
        
        for frameN in range(total_frames):
            if use_custom:
                # Custom stimuli mode
                for i, pattern in enumerate(self.patterns):
                    if pattern[frameN % len(pattern)] == 1 and self.custom_stim_on[i] is not None:
                        self.custom_stim_on[i].draw()
                    elif pattern[frameN % len(pattern)] == 0 and self.custom_stim_off[i] is not None:
                        self.custom_stim_off[i].draw()
                    
                    if self.config.SHOW_LABELS and i < len(self.labels):
                        self.labels[i].draw()
            else:
                # Default mode with opacity
                for i, (stim, pattern) in enumerate(zip(self.stimuli, self.patterns)):
                    stim.opacity = 1.0 if pattern[frameN % len(pattern)] == 1 else 0.0
                    stim.draw()
                    
                    if self.config.SHOW_LABELS and i < len(self.labels):
                        self.labels[i].draw()
            
            flip_time = self.win.flip()
            
            # Call user-provided callback if configured
            if self.config.FLIP_CALLBACK is not None:
                try:
                    self.config.FLIP_CALLBACK(frameN, flip_time)
                except Exception as e:
                    logging.warning(f"Flip callback error at frame {frameN}: {e}")
        
        self.win.recordFrameIntervals = False
        
        # Report results
        self.log_report()
        logging.info("Experiment ended.")
        
        return self.get_report()


class SSVEPExperiment(FlickerExperiment):
    """SSVEP (frequency-based) flickering experiment."""
    
    def __init__(self, config=None):
        """
        Initialize SSVEP experiment.
        
        Args:
            config: SSVEPConfig instance (optional, uses default if not provided)
        
        Raises:
            TypeError: If config is not a SSVEPConfig instance
        """
        if config is None:
            config = SSVEPConfig()
        if not isinstance(config, SSVEPConfig):
            raise TypeError(f"SSVEPExperiment requires SSVEPConfig, got {type(config).__name__}")
        super().__init__(config)
        self.frequencies = []

        
    def prepare_stimuli(self):
        """Calculate frequencies and create all stimuli."""
        # Use custom frequencies if provided, otherwise calculate
        if self.config.CUSTOM_FREQUENCIES is not None:
            self.frequencies = list(self.config.CUSTOM_FREQUENCIES)
            logging.info(f"Using custom frequencies (Hz): {[round(f, 3) for f in self.frequencies]}")
        else:
            self.frequencies = calculate_frequencies(
                self.config.REFRESH_RATE,
                self.config.MIN_FRAMES_PER_CYCLE,
                self.config.N_STIM
            )
            logging.info(f"Auto-calculated frequencies (Hz): {[round(f, 3) for f in self.frequencies]}")
        
        # Calculate positions
        positions = generate_positions(self.config.N_STIM)
        
        # Create stimuli and patterns
        for i, freq in enumerate(self.frequencies):
            frames_per_cycle, on_frames = calculate_cycle_params(
                self.config.REFRESH_RATE, 
                freq, 
                self.config.DUTY_CYCLE
            )
            
            # Create stimulus and label
            self._create_stimulus_at_position(positions[i], i, f"{freq:.2f} Hz")
            
            # Generate pattern (one cycle only)
            pattern = generate_frame_pattern(frames_per_cycle, on_frames)
            self.patterns.append(pattern)
            
            logging.info(f"Stim {i+1}: {freq:.2f} Hz → {frames_per_cycle} frames/cycle "
                        f"({on_frames} ON, {frames_per_cycle - on_frames} OFF)")
    
    def get_experiment_info(self):
        """Get experiment configuration info for logging."""
        return (f"N_STIM={self.config.N_STIM}, DURATION={self.config.DURATION_S}s, "
                f"REFRESH_RATE={self.config.REFRESH_RATE}Hz, MIN_FRAMES={self.config.MIN_FRAMES_PER_CYCLE}")


class CVEPExperiment(FlickerExperiment):
    """c-VEP (code-modulated) flickering experiment."""
    
    def __init__(self, config=None):
        """
        Initialize c-VEP experiment.
        
        Args:
            config: CVEPConfig instance (optional, uses default if not provided)
        
        Raises:
            TypeError: If config is not a CVEPConfig instance
        """
        if config is None:
            config = CVEPConfig()
        if not isinstance(config, CVEPConfig):
            raise TypeError(f"CVEPExperiment requires CVEPConfig, got {type(config).__name__}")
        super().__init__(config)
    
    def prepare_stimuli(self):
        """Create stimuli with m-sequence patterns."""
        # Calculate positions
        positions = generate_positions(self.config.N_STIM)
        
        # Generate m-sequences
        self.patterns = calculate_m_sequences(
            self.config.N_STIM,
            nbits=self.config.NBITS,
            shift_step=self.config.SHIFT_STEP
        )
        
        # Create stimuli
        for i in range(self.config.N_STIM):
            self._create_stimulus_at_position(positions[i], i, f"{i}")
    
    def get_experiment_info(self):
        """Get experiment configuration info for logging."""
        return (f"N_STIM={self.config.N_STIM}, DURATION={self.config.DURATION_S}s, "
                f"REFRESH_RATE={self.config.REFRESH_RATE}Hz, NBITS={self.config.NBITS}, "
                f"SHIFT_STEP={self.config.SHIFT_STEP}")
