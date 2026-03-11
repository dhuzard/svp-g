import pytest
import os
import csv
from src.unit_6 import main

def test_full_pipeline_execution(tmp_path):
    """Test the CLI orchestration with a sample CSV."""
    # Create sample CSV
    csv_file = tmp_path / "tracking.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['t', 'x', 'y'])
        # 30 frames of stationary data (0.1 cm/s)
        for i in range(30):
            # Distance = vel * dt = 0.1 * (1/30) = 0.0033
            writer.writerow([i/30.0, i*0.0033, 0.0])
            
    output_report = tmp_path / "report.csv"
    output_ethogram = tmp_path / "ethogram.png"
    output_matrix = tmp_path / "matrix.png"
    
    # Run CLI
    args = [
        str(csv_file),
        "--report", str(output_report),
        "--ethogram", str(output_ethogram),
        "--matrix", str(output_matrix)
    ]
    
    exit_code = main(args)
    
    assert exit_code == 0
    assert os.path.exists(output_report)
    assert os.path.exists(output_ethogram)
    assert os.path.exists(output_matrix)

def test_cli_outlier_warning(tmp_path, capsys):
    """Verify that a warning is printed if outliers are present."""
    csv_file = tmp_path / "outliers.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['t', 'x', 'y'])
        # Need at least 10 frames for default window
        for i in range(9):
            writer.writerow([i/30.0, 0.0, 0.0])
        # Add an outlier
        writer.writerow([10/30.0, 5.0, 0.0]) # Fast jump
        
    args = [str(csv_file), "--report", str(tmp_path / "out_report.csv")]
    main(args)
    
    captured = capsys.readouterr()
    assert "WARNING: Outliers detected" in captured.out

def test_cli_invalid_file():
    """Verify CLI failure on non-existent file."""
    assert main(["non_existent.csv"]) != 0
