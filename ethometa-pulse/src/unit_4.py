import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from typing import List

def generate_ethogram(states: List[str], timestamps: List[float], output_path: str) -> bool:
    """
    Generates a PNG ethogram plot.
    """
    if not states or not timestamps or len(states) != len(timestamps):
        return False
        
    # Map states to numerical values for plotting
    mapping = {'Stationary': 0, 'Exploration': 1, 'Rapid Movement': 2}
    y_values = [mapping.get(s, -1) for s in states]
    
    # Check for invalid states
    if any(y == -1 for y in y_values):
        return False
        
    plt.figure(figsize=(12, 4))
    
    # Custom color map
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] # Blue, Orange, Green
    cmap = mcolors.ListedColormap(colors)
    
    # Use fill_between for a better ethogram look
    for i in range(len(states) - 1):
        plt.fill_between([timestamps[i], timestamps[i+1]], 0, 1, 
                         color=colors[y_values[i]], step='post')
                         
    plt.yticks([])
    plt.xlabel('Time (s)')
    plt.title('Ethogram: Behavioral States Over Time')
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors[0], label='Stationary'),
                       Patch(facecolor=colors[1], label='Exploration'),
                       Patch(facecolor=colors[2], label='Rapid Movement')]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return True

def generate_transition_matrix(states: List[str], output_path: str) -> bool:
    """
    Generates a PNG transition frequency heatmap.
    """
    if not states or len(states) < 2:
        return False
        
    labels = ['Stationary', 'Exploration', 'Rapid Movement']
    label_to_idx = {l: i for i, l in enumerate(labels)}
    
    matrix = np.zeros((3, 3), dtype=int)
    
    for i in range(len(states) - 1):
        curr = states[i]
        nxt = states[i+1]
        if curr != nxt: # Only count state changes
            if curr in label_to_idx and nxt in label_to_idx:
                matrix[label_to_idx[curr]][label_to_idx[nxt]] += 1
                
    plt.figure(figsize=(8, 6))
    plt.imshow(matrix, cmap='YlOrRd')
    
    plt.xticks(np.arange(3), labels)
    plt.yticks(np.arange(3), labels)
    plt.xlabel('To State')
    plt.ylabel('From State')
    plt.title('Transition Frequency Matrix')
    
    # Add counts to the heatmap
    for i in range(3):
        for j in range(3):
            plt.text(j, i, str(matrix[i, j]), ha='center', va='center', color='black')
            
    plt.colorbar(label='Frequency')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return True
