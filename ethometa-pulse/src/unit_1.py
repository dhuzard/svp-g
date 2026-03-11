import csv
import math
import os
from typing import List, Dict, Any

def load_tracking_data(file_path: str) -> List[Dict[str, float]]:
    """
    Loads CSV tracking data, validates columns, and skips NaN rows.
    
    Required columns: 't', 'x', 'y'
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    required_columns = {'t', 'x', 'y'}
    loaded_data: List[Dict[str, float]] = []
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Validate columns
        if not reader.fieldnames or not required_columns.issubset(set(reader.fieldnames)):
            raise ValueError(f"CSV is missing required columns: {required_columns}")
            
        for row in reader:
            try:
                # Extract and convert values
                t = float(row['t'])
                x = float(row['x'])
                y = float(row['y'])
                
                # Skip if any value is NaN
                if math.isnan(t) or math.isnan(x) or math.isnan(y):
                    continue
                    
                loaded_data.append({'t': t, 'x': x, 'y': y})
            except (ValueError, TypeError):
                # Skip rows with non-numeric data that can't be converted
                continue
                
    return loaded_data
