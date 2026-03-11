import pytest
import os
from src.unit_4 import generate_ethogram, generate_transition_matrix

def test_generate_ethogram_file():
    """Test ethogram PNG generation."""
    states = ['Stationary'] * 10 + ['Exploration'] * 10 + ['Rapid Movement'] * 10
    timestamps = [float(i/30.0) for i in range(30)]
    output_path = "test_ethogram.png"
    
    try:
        success = generate_ethogram(states, timestamps, output_path)
        assert success is True
        assert os.path.exists(output_path)
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

def test_generate_transition_matrix_file():
    """Test transition frequency heatmap PNG generation."""
    states = ['Stationary', 'Exploration', 'Stationary', 'Rapid Movement', 'Exploration']
    output_path = "test_transition_matrix.png"
    
    try:
        success = generate_transition_matrix(states, output_path)
        assert success is True
        assert os.path.exists(output_path)
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

def test_visualization_handles_empty_data():
    """Test that visualization functions return False for empty input."""
    assert generate_ethogram([], [], "empty.png") is False
    assert generate_transition_matrix([], "empty.png") is False
