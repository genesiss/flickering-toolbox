import math
import pytest
import itertools
from src.flicker_core import calculate_frequencies, calculate_cycle_params, generate_positions, generate_frame_pattern

# ==== Test frequency generation ====

@pytest.mark.parametrize("refresh_rate,min_frames_per_cycle,n_stim", [(60, 3, 5), (60, 1, 10), (60, 7, 50), (90, 5, 10), (120, 1, 7), (120, 10, 111)])
def test_frequency_generation(refresh_rate, min_frames_per_cycle, n_stim):
    freqs = calculate_frequencies(refresh_rate, min_frames_per_cycle, n_stim)
    assert len(freqs) == n_stim, "Number of frequencies should be the same as number of stimuli"

    for i in range(n_stim):
        assert freqs[i] == pytest.approx(refresh_rate/(min_frames_per_cycle + i))

def test_refresh_rate_must_be_positive():
    """Should raise AssertionError if refresh_rate <= 0."""
    with pytest.raises(AssertionError, match="refresh_rate must be bigger than zero"):
        calculate_frequencies(refresh_rate=0, min_frames_per_cycle=3, n_stim=5)
    with pytest.raises(AssertionError, match="refresh_rate must be bigger than zero"):
        calculate_frequencies(refresh_rate=-60, min_frames_per_cycle=3, n_stim=5)


def test_min_frames_per_cycle_must_be_positive():
    """Should raise AssertionError if min_frames_per_cycle <= 0."""
    with pytest.raises(AssertionError, match="min_frames_per_cycle must be bigger than zero"):
        calculate_frequencies(refresh_rate=60, min_frames_per_cycle=0, n_stim=5)
    with pytest.raises(AssertionError, match="min_frames_per_cycle must be bigger than zero"):
        calculate_frequencies(refresh_rate=60, min_frames_per_cycle=-1, n_stim=5)


def test_n_stim_must_be_positive():
    """Should raise AssertionError if n_stim <= 0."""
    with pytest.raises(AssertionError, match="n_stim must be bigger than zero"):
        calculate_frequencies(refresh_rate=60, min_frames_per_cycle=3, n_stim=0)
    with pytest.raises(AssertionError, match="n_stim must be bigger than zero"):
        calculate_frequencies(refresh_rate=60, min_frames_per_cycle=3, n_stim=-10)


def test_too_many_stimuli_for_refresh_rate():
    """Should raise AssertionError if n_stim is too large for given refresh_rate."""
    with pytest.raises(AssertionError, match="Too many stimuli provided"):
        calculate_frequencies(refresh_rate=60, min_frames_per_cycle=3, n_stim=100)
    with pytest.raises(AssertionError, match="Too many stimuli provided"):
        calculate_frequencies(refresh_rate=60, min_frames_per_cycle=3, n_stim=59)                   

# ==== Test cycles calculation ====

@pytest.mark.parametrize(
    "refresh_rate,freq,duty_cycle",
    [
        (60, 10, 0.5),
        (60, 12, 0.25),
        (60, 15, 0.75),
        (90, 15, 0.5),
        (120, 10, 0.5),
        (120, 20, 0.25),
        (120, 30, 0.5),
        (120, 6, 0.75),
    ]
)
def test_cycle_param_consistency(refresh_rate, freq, duty_cycle):
    """Verify frames per cycle and ON frame count behave consistently across refresh rates."""
    frames_per_cycle, on_frames = calculate_cycle_params(refresh_rate, freq, duty_cycle)

    # frequency must be reconstructed within ±0.0001 Hz tolerance
    reconstructed_freq = refresh_rate / frames_per_cycle
    assert abs(reconstructed_freq - freq) < 0.0001, \
        f"Expected ~{freq} Hz but got {reconstructed_freq:.4f} Hz"

    # at least one ON and one OFF frame
    assert 1 <= on_frames < frames_per_cycle, "Invalid ON/OFF ratio"

    # check ON frame count roughly matches duty ratio - 
    actual_duty = on_frames / frames_per_cycle
    assert math.isclose(actual_duty, duty_cycle, rel_tol=0.3), \
        f"Duty mismatch: expected {duty_cycle}, got {actual_duty:.2f}"


# ==== Test stable frequencies ====

@pytest.mark.parametrize("refresh_rate, min_frames_per_cycle, n_stim", [(60, 3, 9), (90, 2, 15), (120, 10, 20)])
def test_frequency_generation_is_stable(refresh_rate, min_frames_per_cycle, n_stim):
    """Check that generated frequencies always divide the refresh rate evenly."""
    freqs = calculate_frequencies(refresh_rate, min_frames_per_cycle, n_stim)
    for f in freqs:
        frames = refresh_rate / f
        assert abs(round(frames) - frames) < 1e-6, f"{f} Hz does not evenly divide {refresh_rate} Hz"


def generate_onoff_sequence(frames_per_cycle, on_frames, total_frames):
    """
    Generate the expected binary ON/OFF pattern for a given flicker configuration.
    1 = ON, 0 = OFF
    """
    pattern = [1]*on_frames + [0]*(frames_per_cycle - on_frames)
    return list(itertools.islice(itertools.cycle(pattern), total_frames))   # cycle the pattern, take first total_frames elements from it and return them as list


@pytest.mark.parametrize(
    "refresh_rate,freq,duty_cycle,duration_s",
    [
        (60, 9, 0.5, 120.0),
        (60, 10, 0.5, 1.0),
        (60, 15, 0.33, 1.0),
        (120, 20, 0.5, 1.0),
        (120, 6, 0.25, 1.0)
    ]
)
def test_flicker_onoff_sequence(refresh_rate, freq, duty_cycle, duration_s):
    """
    Verify that the flicker cycle produces the expected ON/OFF pattern.
    """
    frames_per_cycle, on_frames = calculate_cycle_params(refresh_rate, freq, duty_cycle)
    total_frames = int(refresh_rate * duration_s)

    expected = generate_onoff_sequence(frames_per_cycle, on_frames, total_frames)
    actual = generate_frame_pattern(frames_per_cycle, on_frames, total_frames)

    assert expected == actual


