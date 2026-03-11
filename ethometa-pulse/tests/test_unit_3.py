import pytest
from src.unit_3 import classify_behavior

def test_basic_thresholds():
    """Test classification based on thresholds without bout filter."""
    # Sampling rate 30Hz, Bout duration 0.0 (off)
    data = [
        {'velocity': 0.1}, # Stationary
        {'velocity': 0.6}, # Exploration
        {'velocity': 4.0}, # Rapid Movement
        {'velocity': 12.0} # Rapid Movement (outlier case)
    ]
    states = classify_behavior(data, sampling_rate=30.0, bout_duration=0.0)
    
    assert states[0] == 'Stationary'
    assert states[1] == 'Exploration'
    assert states[2] == 'Rapid Movement'
    assert states[3] == 'Rapid Movement'

def test_bout_duration_filter():
    """Test 0.3s minimum bout duration filter."""
    # 0.3s at 30Hz is 9 frames. 
    # A state change must last at least 9 frames.
    
    # Start with 20 frames of Stationary
    data = [{'velocity': 0.1}] * 20
    
    # Add 5 frames of Exploration (less than 9)
    data += [{'velocity': 1.0}] * 5
    
    # Add 20 frames of Stationary
    data += [{'velocity': 0.1}] * 20
    
    # Total 45 frames. The 5 frames of Exploration should be suppressed.
    states = classify_behavior(data, sampling_rate=30.0, bout_duration=0.3)
    
    assert len(states) == 45
    for s in states:
        assert s == 'Stationary'

def test_bout_duration_accepted():
    """Test that state changes lasting exactly or more than bout_duration are kept."""
    # 9 frames is exactly 0.3s at 30Hz
    data = [{'velocity': 0.1}] * 20
    data += [{'velocity': 1.0}] * 9
    data += [{'velocity': 0.1}] * 20
    
    states = classify_behavior(data, sampling_rate=30.0, bout_duration=0.3)
    
    assert states[19] == 'Stationary'
    assert states[20] == 'Exploration'
    assert states[28] == 'Exploration'
    assert states[29] == 'Stationary'

def test_outlier_classification():
    """Verify that velocity > 10 is classified as Rapid Movement."""
    data = [{'velocity': 15.0}] * 10
    states = classify_behavior(data, sampling_rate=30.0, bout_duration=0.0)
    for s in states:
        assert s == 'Rapid Movement'

def test_empty_or_invalid():
    """Test error handling."""
    with pytest.raises(ValueError):
        classify_behavior([], sampling_rate=-1)
