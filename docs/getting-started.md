# Installation

## Prerequisites

- **Python 3.8 or higher**
- **A compatible monitor** (60Hz, 120Hz, or 240Hz refresh rate)
- Basic knowledge of Python programming

## Installing

Clone the repository and install:

```bash
git clone https://github.com/genesiss/flickering-toolbox.git
cd flickering-toolbox
pip install -r requirements.txt
```

## Verifying Installation 

Test that everything is working:

```bash
python -c "from src import SSVEPExperiment; print('✅ Installation successful!')"
```

Run the test suite:

```bash
python -m pytest tests/
```

You should see output like:
```
======================== 26 passed in 19.19s ========================
```

## System Configuration

### Monitor Refresh Rate

**Critical**: You must know your monitor's refresh rate. Check in your system settings:

=== "macOS"
    1. Open **System Settings**
    2. Go to **Displays** → **Display Settings**
    3. Note the **Refresh Rate** (typically 60Hz, 120Hz, or 240Hz)

=== "Windows"
    1. Open **Settings** → **System** → **Display**
    2. Click **Advanced display settings**
    3. Note the **Refresh rate**

=== "Linux"
    ```bash
    xrandr | grep "*"
    ```
    Look for the value with an asterisk (e.g., "60.00*")

!!! warning "Important"
    Using an incorrect refresh rate in your configuration will cause timing errors and invalidate your experimental results!

### Display Settings

For best results:

- **Disable power saving** - Prevent screen dimming during experiments
- **Disable notifications** - Avoid interruptions
- **Close background apps** - Reduce system load
- **Use fullscreen mode** - More stable timing
- **Disable variable refresh rate** - some monitors (for example Mac M1 PRO (2021)) use variable refresh rate. Make sure to disable it and force a fixed refresh rate.
- **Enable VSync** - ensure that VSync is enabled, since this guarantees that the framebuffer is swapped only during the VBlank interval.
- **Disable tripple buffering** - in Windows 10 this must be manually disabled, usually in the GPU control panel under 3D or OpenGL settings.

## Next Steps

Now that you're set up, proceed to the [Quick Start Guide](quick-start.md) to run your first experiment!
