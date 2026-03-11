# Stakeholder Specification: EthoMeta-Pulse

## 1. Project Overview
EthoMeta-Pulse is a behavioral neuroscience tool designed to process CSV-based animal tracking data (t, x, y) to compute instantaneous kinematics and classify behavioral states based on velocity.

## 2. Functional Requirements

### 2.1 Data Import
- **Input Format:** CSV file containing at least three columns: `t` (timestamp or frame index), `x` (x-coordinate), and `y` (y-coordinate).
- **Sampling Rate:** 30 Hz (default).
- **Coordinate System:** Physical units (cm), with a standard arena size of 100cm x 100cm.
- **Missing Data:** Rows containing NaN or null values in `t`, `x`, or `y` must be skipped (not interpolated).

### 2.2 Kinematic Calculations
- **Velocity:** Compute instantaneous velocity (cm/s) between consecutive valid frames.
- **Acceleration:** Compute instantaneous acceleration (cm/s²) based on velocity changes.
- **Smoothing:** Apply a rolling mean filter to `x` and `y` coordinates to reduce tracking jitter. The default window size is **10 frames**.

### 2.3 Behavioral Classification
Classify each frame into one of three states based on the smoothed velocity:
- **Stationary:** 0.0 ≤ velocity < 0.5 cm/s
- **Exploration:** 0.5 ≤ velocity < 3.0 cm/s
- **Rapid Movement:** 3.0 ≤ velocity ≤ 10.0 cm/s

### 2.4 State Transition Logic
- **Bout Duration:** A state must persist for a minimum of **0.3 seconds** (9 frames at 30Hz) to be recorded as a state change. Transitions shorter than this threshold are ignored, and the previous state is maintained to prevent high-frequency noise ("chatter") in the ethogram.

### 2.5 Outlier Handling
- **Threshold:** Any computed velocity **> 10 cm/s** is considered an outlier.
- **Action:** Flag outliers in a final report; issue a console warning at the end of processing but do not halt execution.

## 3. Output Requirements

### 3.1 Visualizations
- **Ethogram:** A time-series plot (PNG) showing behavioral states over the duration of the trial.
- **Transition Matrix:** A heatmap (PNG) representing the **frequency of transitions** between the three behavioral states.

### 3.2 Data Export
- **Summary Report:** A CSV file containing:
    - Percentage of time spent in each state.
    - Total distance traveled.
    - Outlier count and timestamps.
    - Transition frequency table.

## 4. Acceptance Criteria
1. The tool successfully processes a 30Hz tracking CSV with physical coordinates.
2. The 0.3s bout duration filter correctly eliminates sub-threshold state flickers.
3. Outliers > 10 cm/s are accurately reported in the CSV summary.
4. PNG visualizations are generated for both the ethogram and the transition matrix.
