import math
from typing import List, Dict

def classify_behavior(
    data: List[Dict[str, float]], 
    sampling_rate: float = 30.0,
    bout_duration: float = 0.3
) -> List[str]:
    """
    Classifies behavioral states based on velocity and filters transitions 
    using a minimum bout duration.
    """
    if sampling_rate <= 0:
        raise ValueError("sampling_rate must be positive.")
    if bout_duration < 0:
        raise ValueError("bout_duration cannot be negative.")
        
    if not data:
        return []

    # 1. Initial Threshold-Based Classification
    raw_states = []
    for row in data:
        v = row.get('velocity', 0.0)
        if v < 0.5:
            raw_states.append('Stationary')
        elif 0.5 <= v < 3.0:
            raw_states.append('Exploration')
        else: # v >= 3.0 (including outliers > 10.0)
            raw_states.append('Rapid Movement')

    if bout_duration == 0:
        return raw_states

    # 2. Minimum Bout Duration Filter
    # 0.3s at 30Hz is 9 frames
    min_frames = math.ceil(bout_duration * sampling_rate)
    filtered_states = raw_states.copy()
    
    i = 0
    while i < len(filtered_states):
        current_state = filtered_states[i]
        
        # Find the length of the current bout
        j = i
        while j < len(filtered_states) and filtered_states[j] == current_state:
            j += 1
        
        bout_length = j - i
        
        # If bout is too short and not the very first bout
        if bout_length < min_frames and i > 0:
            # Revert to the previous stable state
            prev_state = filtered_states[i-1]
            for k in range(i, j):
                filtered_states[k] = prev_state
            # After modification, we don't increment i, but j, 
            # because we might have merged this bout with the previous one.
            # But actually, if we revert to prev_state, the entire [i, j) 
            # range is now prev_state. We should re-evaluate from the next bout.
            i = j
        else:
            i = j
            
    return filtered_states
