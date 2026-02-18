# SSVEP vs c-VEP Paradigms

Understanding the two visual evoked potential paradigms supported by Flickering Toolbox.

## Overview

Both SSVEP and c-VEP are brain-computer interface (BCI) paradigms that use visual stimulation to elicit neural responses. They differ in **how** the stimuli are modulated.

| Feature | SSVEP | c-VEP |
|---------|-------|-------|
| **Modulation** | Frequency-based | Pattern-based (m-sequences) |
| **Frequencies** | Different for each stimulus | All use same pattern, shifted |
| **Bandwidth** | Requires wide bandwidth | Efficient bandwidth usage |
| **Max stimuli** | Limited by freq. spacing | More stimuli possible |

## SSVEP (Steady-State Visual Evoked Potential)

### Principle

Each stimulus flickers at a **unique frequency**. When you look at a stimulus, your brain generates a response at that frequency.

```
Stimulus 1: 20Hz ───┐  ┌───┐  ┌───┐  ┌───
                    └──┘  └──┘  └──┘  └──

Stimulus 2: 15Hz ─────┐   ┌─────┐   ┌───
                      └───┘     └───┘   

Stimulus 3: 12Hz ───────┐    ┌───────┐  
                        └────┘       └──
```

### How It Works

1. **Stimulus**: Flickering at frequency f (e.g., 15 Hz)
2. **Neural response**: EEG shows activity at f and harmonics (2f, 3f, ...)
3. **Detection**: FFT of EEG signal peaks at f
4. **Classification**: Identify which frequency has strongest response

## c-VEP (code-modulated Visual Evoked Potential)

### Principle

All stimuli use the **same binary pattern** (m-sequence), but **time-shifted**. Brain responses are classified by correlation with known patterns.

```
Base m-sequence: 1 0 1 1 1 0 1 0 0 1 1 0 0 0 1 ...

Stimulus 1: 1 0 1 1 1 0 1 0 0 1 1 0 0 0 1 ... (shift 0)
Stimulus 2: 0 0 0 1 0 1 1 1 0 1 0 0 1 1 0 ... (shift 4)  
Stimulus 3: 1 1 0 0 0 1 0 1 1 1 0 1 0 0 1 ... (shift 8)
```

### How It Works

1. **Stimulus**: Binary pattern from m-sequence
2. **Neural response**: Transient VEP to each transition
3. **Detection**: Cross-correlation with template patterns
4. **Classification**: Highest correlation indicates gazed stimulus

## Next Steps

- Try [Examples](examples.md) for both paradigms
- Check [Configuration](configuration.md) for parameter details
- See [API Reference](api-core.md) for implementation
