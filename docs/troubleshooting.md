# Troubleshooting

Solutions to common problems and issues.

## Frame Timing Issues

### Many Dropped Frames

**Symptoms:**
Console logs show low stability and a lot of dropped frames.

```
Dropped frames: 45
Stability percent: 85.00%
```

**Causes and Solutions:**

#### 1. Incorrect Refresh Rate

**Problem:**
```python
config.REFRESH_RATE = 60.0  # But monitor is actually 120Hz!
```

**Solution:** Verify actual refresh rate in system settings. Then update configuration:
```python
config.REFRESH_RATE = 120.0
```

#### 2. Not Using Fullscreen

**Problem:**
```python
config.FULLSCREEN = False  # Windowed mode
```

**Solution:** Use fullscreen:
```python
config.FULLSCREEN = True
```

#### 3. Background Applications

**Problem:** Other apps consuming CPU/GPU

**Solution:** Close unnecessary applications:
- Web browsers
- Video players
- IDE debuggers
- Background updates
- If using a laptop, check that it is not in power save mode

#### 4. Too Many Stimuli

 **Problem:** System can't render all stimuli in time

**Solution:** Reduce number of stimuli:
```python
config.N_STIM = 4
```

---

## Configuration Errors

### "Too many stimuli provided"

**Error Message:**
```
AssertionError: Too many stimuli provided for given refresh_rate 
and min_frames_per_cycle. Maximum number of allowed stimuli is 58
```

**Cause:** `N_STIM` exceeds capacity

**Solution:**

Calculate maximum:
```python
max_stim = config.REFRESH_RATE - config.MIN_FRAMES_PER_CYCLE + 1
```

Options:
1. **Reduce N_STIM:**
   ```python
   config.N_STIM = 6
   ```

2. **Increase MIN_FRAMES_PER_CYCLE:**
   ```python
   config.MIN_FRAMES_PER_CYCLE = 4
   ```

3. **Use higher refresh rate monitor:**
   ```python
   config.REFRESH_RATE = 120.0  # More capacity
   ```

4. **Switch to c-VEP:**
   ```python
   from src import CVEPExperiment, CVEPConfig
   # c-VEP supports more stimuli
   ```

---

### "refresh_rate must be bigger than zero"

**Error Message:**
```
AssertionError: refresh_rate must be bigger than zero. Provided value: 0
```

**Cause:** Invalid refresh rate

**Solution:**
```python
config.REFRESH_RATE = 60.0  # Positive value
```

---

### Import Errors

**Error Message:**
```
ModuleNotFoundError: No module named 'src'
```

**Solutions:**

1. **Run from correct directory:**
   ```bash
   cd /path/to/flickering-toolbox
   python my_experiment.py
   ```

---

### Missing Dependencies

**Error:** `ModuleNotFoundError: No module named 'numpy'`

**Solution:**
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install psychopy numpy scipy
```

## See Also

- [Configuration](configuration.md) - Parameter reference
- [Examples](examples.md) - Working code samples
