import pytest
import csv
import os
import tempfile
from src.unit_1 import load_tracking_data

def create_temp_csv(data: list, columns: list = ['t', 'x', 'y']):
    """Helper to create a temporary CSV file for testing."""
    fd, path = tempfile.mkstemp(suffix='.csv')
    with os.fdopen(fd, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)
    return path

def test_load_valid_csv():
    """Test loading a standard valid tracking CSV."""
    data = [
        {'t': 0.0, 'x': 10.0, 'y': 20.0},
        {'t': 0.033, 'x': 10.5, 'y': 20.5},
        {'t': 0.066, 'x': 11.0, 'y': 21.0}
    ]
    path = create_temp_csv(data)
    try:
        loaded = load_tracking_data(path)
        assert len(loaded) == 3
        assert loaded[0]['t'] == 0.0
        assert loaded[1]['x'] == 10.5
        assert loaded[2]['y'] == 21.0
    finally:
        os.remove(path)

def test_missing_columns():
    """Test that ValueError is raised if columns are missing."""
    data = [{'t': 0.0, 'x': 10.0}]  # Missing 'y'
    path = create_temp_csv(data, columns=['t', 'x'])
    try:
        with pytest.raises(ValueError, match="required columns"):
            load_tracking_data(path)
    finally:
        os.remove(path)

def test_skip_nan_rows():
    """Test that rows with NaN values are skipped."""
    data = [
        {'t': 0.0, 'x': 10.0, 'y': 20.0},
        {'t': 0.033, 'x': float('nan'), 'y': 20.5},  # Should skip
        {'t': 0.066, 'x': 11.0, 'y': 21.0}
    ]
    path = create_temp_csv(data)
    try:
        loaded = load_tracking_data(path)
        assert len(loaded) == 2
        assert loaded[0]['t'] == 0.0
        assert loaded[1]['t'] == 0.066
    finally:
        os.remove(path)

def test_file_not_found():
    """Test that FileNotFoundError is raised for non-existent paths."""
    with pytest.raises(FileNotFoundError):
        load_tracking_data("non_existent_file.csv")

def test_temporal_order():
    """Test that temporal order of rows is preserved."""
    data = [
        {'t': 0.066, 'x': 11.0, 'y': 21.0},
        {'t': 0.0, 'x': 10.0, 'y': 20.0},
        {'t': 0.033, 'x': 10.5, 'y': 20.5}
    ]
    path = create_temp_csv(data)
    try:
        loaded = load_tracking_data(path)
        assert loaded[0]['t'] == 0.066
        assert loaded[1]['t'] == 0.0
        assert loaded[2]['t'] == 0.033
    finally:
        os.remove(path)
