# Technical Blueprint: EthoMeta-Pulse

This blueprint decomposes the EthoMeta-Pulse project into six testable units. All units follow the 30Hz sampling rate and 0.3s bout duration constraints.

## Unit 1: Data Loader

**Artifact category:** Utility

### Tier 1 -- Description

Responsible for reading the input CSV file and validating that it contains the required columns (`t`, `x`, `y`). It must skip any rows containing NaN or null values to ensure only valid tracking data is passed downstream.

### Tier 2 — Signatures

```python
from typing import List, Dict, Any

def load_tracking_data(file_path: str) -> List[Dict[str, float]]:
    """Loads CSV tracking data, validates columns, and skips NaN rows."""
    pass
```

### Tier 2 — Invariants

```python
# Assert that 't', 'x', and 'y' are present in every returned row
# Assert that no row contains None or NaN values
```

### Tier 3 -- Error Conditions

- `FileNotFoundError`: If the input path does not exist.
- `ValueError`: If the CSV is missing the required columns (`t`, `x`, `y`).

### Tier 3 -- Behavioral Contracts

- Skips all rows containing at least one NaN value.
- Preserves the temporal order of rows as found in the CSV.

### Tier 3 -- Dependencies

- None.

---

## Unit 2: Kinematic Calculator

**Artifact category:** Core Logic

### Tier 1 -- Description

Computes instantaneous velocity and acceleration from the tracking data. It first applies a 10-frame rolling mean to the `x` and `y` coordinates to reduce jitter before performing the calculations.

### Tier 2 — Signatures

```python
from typing import List, Dict

def calculate_kinematics(
    data: List[Dict[str, float]], 
    window_size: int = 10
) -> List[Dict[str, float]]:
    """Applies rolling mean and computes velocity/acceleration for each frame."""
    pass
```

### Tier 2 — Invariants

```python
# Assert velocity is >= 0
# Assert output length matches input length (ignoring first few frames of rolling mean if necessary)
```

### Tier 3 -- Error Conditions

- `ValueError`: If the data has fewer than `window_size` frames.

### Tier 3 -- Behavioral Contracts

- Uses Euclidean distance for velocity calculation.
- Velocity is in units of cm/s based on the 30Hz sampling rate (1/30s intervals).
- Acceleration is in cm/s².
- Rolling mean must be "centered" or "forward-looking" as per standard behavioral analysis conventions (clarification: will use standard centered rolling mean).

### Tier 3 -- Dependencies

- Unit 1: Data Loader

---

## Unit 3: Behavioral Classifier

**Artifact category:** Core Logic

### Tier 1 -- Description

Classifies each frame into 'Stationary', 'Exploration', or 'Rapid Movement' based on velocity thresholds. It applies a 0.3s (9 frames) minimum bout duration filter to prevent high-frequency state switching.

### Tier 2 — Signatures

```python
from typing import List, Dict

def classify_behavior(
    data: List[Dict[str, float]], 
    sampling_rate: float = 30.0,
    bout_duration: float = 0.3
) -> List[str]:
    """Assigns behavioral states to frames using thresholds and a minimum bout filter."""
    pass
```

### Tier 2 — Invariants

```python
# Assert all labels are one of: 'Stationary', 'Exploration', 'Rapid Movement'
# Assert output length matches input length
```

### Tier 3 -- Error Conditions

- `ValueError`: If invalid sampling rate or bout duration is provided.

### Tier 3 -- Behavioral Contracts

- Thresholds: Stationary (<0.5), Exploration (0.5-3.0), Rapid Movement (3.0-10.0).
- Any state shorter than 0.3s is reverted to the previous state.
- Velocities > 10 cm/s are classified as 'Rapid Movement' for the purpose of the ethogram but noted for outlier reporting.

### Tier 3 -- Dependencies

- Unit 2: Kinematic Calculator

---

## Unit 4: Visualization Suite

**Artifact category:** Output

### Tier 1 -- Description

Generates visual representations of the behavioral data. This includes an Ethogram (state vs. time) and a Transition Frequency Matrix (heatmap).

### Tier 2 — Signatures

```python
from typing import List

def generate_ethogram(states: List[str], timestamps: List[float], output_path: str) -> bool:
    """Generates a PNG ethogram plot."""
    pass

def generate_transition_matrix(states: List[str], output_path: str) -> bool:
    """Generates a PNG transition frequency heatmap."""
    pass
```

### Tier 3 -- Behavioral Contracts

- Ethogram must use distinct colors for each of the three states.
- Transition matrix must show counts (frequencies) of transitions between states.
- Files must be saved as PNG.

### Tier 3 -- Dependencies

- Unit 3: Behavioral Classifier

---

## Unit 5: Report Generator

**Artifact category:** Output

### Tier 1 -- Description

Calculates summary statistics for the trial and exports them to a CSV file. It identifies and reports outliers (velocity > 10 cm/s).

### Tier 2 — Signatures

```python
from typing import List, Dict

def generate_summary_report(
    data: List[Dict[str, float]], 
    states: List[str], 
    output_path: str
) -> Dict[str, Any]:
    """Computes stats and writes a CSV summary report."""
    pass
```

### Tier 3 -- Behavioral Contracts

- Computes: % time in state, total distance (cm), and outlier count.
- CSV must include timestamps for all outliers (>10 cm/s).
- Returns a dictionary of summary statistics for use by the CLI.

### Tier 3 -- Dependencies

- Unit 3: Behavioral Classifier

---

## Unit 6: Main CLI

**Artifact category:** Entry Point

### Tier 1 -- Description

The main command-line interface that orchestrates the entire pipeline. It handles user inputs (file paths, parameters) and outputs terminal warnings if outliers are detected.

### Tier 2 — Signatures

```python
def main(args: List[str]) -> int:
    """Orchestrates the data loading, calculation, classification, and output."""
    pass
```

### Tier 3 -- Behavioral Contracts

- Prints a console warning at the end if the outlier count is > 0.
- Coordinates the flow of data from Unit 1 through Unit 5.
- Exits with code 0 on success, non-zero on failure.

### Tier 3 -- Dependencies

- Units 1-5.
