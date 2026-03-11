import pytest
import math
from src.unit_2 import calculate_kinematics

def test_rolling_mean_simple():
    """Test 10-frame rolling mean jitter reduction."""
    # Create 20 frames of data with constant jitter
    data = []
    for i in range(20):
        # Base x=100.0, jitter +/- 1.0
        jitter = 1.0 if i % 2 == 0 else -1.0
        data.append({'t': i/30.0, 'x': 100.0 + jitter, 'y': 0.0})
    
    results = calculate_kinematics(data, window_size=10)
    
    # Check middle frames (where window is full)
    # Average of [+1, -1, +1, -1, +1, -1, +1, -1, +1, -1] is 0
    # So smoothed x should be exactly 100.0
    for i in range(5, 15):
        assert pytest.approx(results[i]['x'], abs=1e-5) == 100.0

def test_velocity_constant_motion():
    """Test velocity computation for constant speed (10 cm/s)."""
    # 30Hz -> 0.0333s intervals
    # To get 10 cm/s, distance must be 10 * 0.0333 = 0.3333 cm per frame
    data = []
    for i in range(20):
        data.append({'t': i/30.0, 'x': i * (10.0/30.0), 'y': 0.0})
        
    results = calculate_kinematics(data, window_size=1) # No smoothing for this test
    
    # Check middle frame velocity
    # Distance = 0.333, dt = 0.0333 -> Vel = 10.0
    for i in range(1, 19):
        assert pytest.approx(results[i]['velocity'], rel=1e-3) == 10.0

def test_acceleration_constant():
    """Test acceleration computation."""
    # Velocity increases by 1 cm/s every frame
    # At 30Hz, dv = 1 cm/s, dt = 1/30s -> Accel = 30 cm/s^2
    data = []
    x = 0.0
    v = 0.0
    dt = 1/30.0
    for i in range(20):
        data.append({'t': i*dt, 'x': x, 'y': 0.0})
        v += 1.0 # velocity at next step
        x += v*dt
        
    results = calculate_kinematics(data, window_size=1)
    
    # Check acceleration (constant 30 cm/s^2)
    for i in range(2, 18):
        assert pytest.approx(results[i]['acceleration'], rel=1e-2) == 30.0

def test_insufficient_data():
    """Test that ValueError is raised for data shorter than window size."""
    data = [{'t': 0.0, 'x': 0.0, 'y': 0.0}]
    with pytest.raises(ValueError, match="fewer than window_size"):
        calculate_kinematics(data, window_size=10)

def test_output_structure():
    """Test that output contains all required keys."""
    data = [{'t': i/30.0, 'x': float(i), 'y': 0.0} for i in range(15)]
    results = calculate_kinematics(data, window_size=5)
    
    assert len(results) == 15
    for row in results:
        assert 'velocity' in row
        assert 'acceleration' in row
        assert 'x' in row
        assert 'y' in row
        assert 't' in row
