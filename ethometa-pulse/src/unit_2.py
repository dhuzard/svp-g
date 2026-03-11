import math
from typing import List, Dict

def calculate_kinematics(
    data: List[Dict[str, float]], 
    window_size: int = 10
) -> List[Dict[str, float]]:
    """
    Applies a centered rolling mean filter to x and y coordinates and computes 
    instantaneous velocity and acceleration.
    """
    if len(data) < window_size:
        raise ValueError(f"Data has fewer than window_size ({window_size}) frames.")

    # 1. Apply Centered Rolling Mean
    smoothed_data = []
    half_window = window_size // 2
    
    for i in range(len(data)):
        # For a centered window of size N:
        # start = i - floor(N/2)
        # end = i + ceil(N/2)
        start = max(0, i - half_window)
        end = min(len(data), i + (window_size - half_window))
        
        window = data[start:end]
        
        mean_x = sum(d['x'] for d in window) / len(window)
        mean_y = sum(d['y'] for d in window) / len(window)
        
        smoothed_data.append({
            't': data[i]['t'],
            'x': mean_x,
            'y': mean_y
        })

    # 2. Compute Velocity and Acceleration
    results = []
    for i in range(len(smoothed_data)):
        row = smoothed_data[i].copy()
        
        # Velocity
        if i == 0:
            velocity = 0.0
        else:
            prev = smoothed_data[i-1]
            curr = smoothed_data[i]
            
            dist = math.sqrt((curr['x'] - prev['x'])**2 + (curr['y'] - prev['y'])**2)
            dt = curr['t'] - prev['t']
            
            if dt > 0:
                velocity = dist / dt
            else:
                velocity = 0.0
        
        row['velocity'] = velocity
        results.append(row)

    # 3. Acceleration (dv/dt)
    for i in range(len(results)):
        if i == 0:
            acceleration = 0.0
        else:
            prev_v = results[i-1]['velocity']
            curr_v = results[i]['velocity']
            dt = results[i]['t'] - results[i-1]['t']
            
            if dt > 0:
                acceleration = (curr_v - prev_v) / dt
            else:
                acceleration = 0.0
        
        results[i]['acceleration'] = acceleration

    return results
