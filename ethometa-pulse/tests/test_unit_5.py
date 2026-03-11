import pytest
import os
import csv
from src.unit_5 import generate_summary_report

def test_generate_summary_report_file():
    """Test summary report CSV generation and stats."""
    data = [
        {'t': 0.0, 'velocity': 0.1},
        {'t': 0.1, 'velocity': 12.0}, # Outlier
        {'t': 0.2, 'velocity': 1.0},
        {'t': 0.3, 'velocity': 0.5}
    ]
    states = ['Stationary', 'Rapid Movement', 'Exploration', 'Exploration']
    output_path = "test_report.csv"
    
    try:
        stats = generate_summary_report(data, states, output_path)
        
        assert os.path.exists(output_path)
        assert stats['outlier_count'] == 1
        assert stats['Stationary_percent'] == 25.0
        assert stats['Exploration_percent'] == 50.0
        assert stats['Rapid Movement_percent'] == 25.0
        
        # Check CSV content
        with open(output_path, 'r') as f:
            reader = csv.DictReader(f)
            # The header is ['Section', 'Key', 'Value'] but it transitions for outliers
            rows = list(reader)
            
            found_outlier = False
            for r in rows:
                # In the implementation: writer.writerow(['Outlier', f"{o['t']:.3f}", f"{o['velocity']:.2f}"])
                # Key maps to 'Section', Value maps to 'Key', and third col to 'Value'
                if r.get('Section') == 'Outlier' and float(r.get('Key', 0)) == 0.1:
                    found_outlier = True
            assert found_outlier is True
            
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

def test_distance_calculation():
    """Verify total distance is computed correctly."""
    # Two movements: (0.1s * 10cm/s) + (0.1s * 20cm/s) = 1 + 2 = 3 cm
    data = [
        {'t': 0.0, 'velocity': 0.0},
        {'t': 0.1, 'velocity': 10.0},
        {'t': 0.2, 'velocity': 20.0}
    ]
    states = ['Stationary', 'Rapid Movement', 'Rapid Movement']
    stats = generate_summary_report(data, states, "temp.csv")
    try:
        assert pytest.approx(stats['total_distance'], rel=1e-3) == 3.0
    finally:
        if os.path.exists("temp.csv"):
            os.remove("temp.csv")

def test_report_invalid_input():
    """Test error handling."""
    with pytest.raises(ValueError):
        generate_summary_report([], [], "fail.csv")
