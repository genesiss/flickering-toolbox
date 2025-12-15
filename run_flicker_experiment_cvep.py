from psychopy import visual, core, logging
from src.flicker_core import calculate_frequencies, calculate_cycle_params, generate_positions, generate_frame_pattern, calculate_m_sequences

# ==== Settings ====
FULLSCREEN = True           # Should the window be opened in full screen mode (preferred, because of expected better performance)
REFRESH_RATE = 60.0         # Refresh rate (make sure that operating system is not using variable refresh rate)
DURATION_S = 5.0            # duration of experiment
N_STIM = 9                  # number of flickering elements
DUTY_CYCLE = 0.5            # represents ratio between ON and OFF stimuli presentation
MIN_FRAMES_PER_CYCLE = 3     # Minimum number of frames that flicker should be in ON state. If MIN_FRAMES_PER_CYCLE is set to 3 and REFRESH_RATE is 60, max frequency of flickering will be 60Hz/3=20Hz.

# ==== Logger ====
logging.console.setLevel(logging.INFO)  # set PsychoPy logging handler console level to INFO, so that we get logging output with frames related messages
logfile = logging.LogFile("flicker_log.txt", level=logging.INFO, filemode='w')
logging.info("===== Starting flickering test =====")

# ==== Window ====
win = visual.Window(
    screen=0,   # id of screen (if using multiple screens)
    size=[1920,1080],   # will be ignored if FULLSCREEN is set to True
    units="norm",
    fullscr=FULLSCREEN,
    color=[0,0,0], # rgb color of window background - black.
    allowGUI=False, # disable GUI
    waitBlanking=True   # make PsychoPy wait for VBlank interval when calling flip(). This means that flip() will block the processing and wait for VBlank interval.
)

logging.info("Window open.")
total_frames = int(REFRESH_RATE * DURATION_S)  # calculate number of total frames based on desired experiment duration


# ==== Calculate stimuli positions ====
positions = generate_positions(N_STIM)

# ==== Create stimuli ====
stimuli, labels = [], []
for i in range(N_STIM):
    stim = visual.Rect(win, width=0.3, height=0.3, fillColor='white', pos=positions[i])  # create a stimuli
    label = visual.TextStim(win, text=f"{i}", pos=positions[i],  # create a label with flickering frequency
                            height=0.05, color='black')
    stimuli.append(stim)
    labels.append(label)


# ==== Main flickering loop ====
frameN = 0

# prepare frame patterns
patterns = calculate_m_sequences(N_STIM, total_frames)

logging.info(f"Starting flickering sequence (Estimated number of frames: {total_frames}).")
win.recordFrameIntervals = True # start recording frame intervals so that we get report of dropped frames
win.refreshThreshold = (1.0 / REFRESH_RATE) + 0.004 # set threshold for marking frame as dropped

for frameN in range(total_frames):
    for (stim, label, pattern) in zip(stimuli, labels, patterns):
        if pattern[frameN % len(pattern)] == 1:
            stim.opacity = 1.0
        else:
            stim.opacity = 0.0
        
        stim.draw()
        label.draw()

    win.flip()
    
win.recordFrameIntervals = False

# ==== Report ====
intervals = win.frameIntervals
logging.info("===== Report =====")
logging.info(f"Dropped frames: {win.nDroppedFrames}")
if intervals:
    mean_int = sum(intervals)/len(intervals)
    sd_int = (sum((i - mean_int)**2 for i in intervals)/len(intervals))**0.5
    stable_percent = 100 * (1 - win.nDroppedFrames / len(intervals))
    logging.info(f"Total frames recorded: {len(intervals)}")
    logging.info(f"Average frame interval: {mean_int*1000:.3f} ms (expected based on refresh rate {1000/REFRESH_RATE:.3f} ms)")
    logging.info(f"SD of frame intervals: {sd_int*1000:.3f} ms")
    logging.info(f"Stabilty percent: {stable_percent:.2f} %")
else:
    logging.warning("No frame intervals recorded!")

logging.info("Experiment ended.")
win.close()
core.quit()
