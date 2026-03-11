import csv
from typing import List, Dict, Any

def generate_summary_report(
    data: List[Dict[str, float]], 
    states: List[str], 
    output_path: str
) -> Dict[str, Any]:
    """
    Computes summary statistics and writes a CSV report.
    """
    if not data or not states or len(data) != len(states):
        raise ValueError("Invalid input: data and states must be non-empty and of equal length.")

    # 1. Compute Basic Stats
    total_frames = len(states)
    state_counts = {}
    for s in states:
        state_counts[s] = state_counts.get(s, 0) + 1
        
    stats = {}
    for s in ['Stationary', 'Exploration', 'Rapid Movement']:
        count = state_counts.get(s, 0)
        stats[f"{s}_percent"] = (count / total_frames) * 100.0
        
    # 2. Total Distance
    total_distance = 0.0
    for i in range(1, len(data)):
        v = data[i].get('velocity', 0.0)
        dt = data[i]['t'] - data[i-1]['t']
        total_distance += v * dt
    stats['total_distance'] = total_distance
    
    # 3. Outliers
    outliers = []
    for row in data:
        if row.get('velocity', 0.0) > 10.0:
            outliers.append(row)
    stats['outlier_count'] = len(outliers)
    
    # 4. Write CSV Report
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Section', 'Key', 'Value'])
        
        # Summary Section
        writer.writerow(['Summary', 'Total Frames', total_frames])
        writer.writerow(['Summary', 'Total Distance (cm)', f"{total_distance:.2f}"])
        writer.writerow(['Summary', 'Outlier Count', len(outliers)])
        
        # States Section
        for s in ['Stationary', 'Exploration', 'Rapid Movement']:
            writer.writerow(['State %', s, f"{stats[f'{s}_percent']:.2f}%"])
            
        # Outliers Section
        if outliers:
            writer.writerow([])
            writer.writerow(['Outlier Report', 'Timestamp', 'Velocity (cm/s)'])
            for o in outliers:
                writer.writerow(['Outlier', f"{o['t']:.3f}", f"{o['velocity']:.2f}"])
                
    return stats
