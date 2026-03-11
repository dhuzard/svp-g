import sys
import argparse
from typing import List

from src.unit_1 import load_tracking_data
from src.unit_2 import calculate_kinematics
from src.unit_3 import classify_behavior
from src.unit_4 import generate_ethogram, generate_transition_matrix
from src.unit_5 import generate_summary_report

def main(args: List[str] = None) -> int:
    """
    Main entry point for EthoMeta-Pulse.
    Orchestrates loading, calculation, classification, and reporting.
    """
    if args is None:
        args = sys.argv[1:]
        
    parser = argparse.ArgumentParser(description="EthoMeta-Pulse: Behavioral Analysis Tool")
    parser.add_argument("input", help="Path to input tracking CSV (t, x, y)")
    parser.add_argument("--report", default="summary_report.csv", help="Output path for CSV report")
    parser.add_argument("--ethogram", default="ethogram.png", help="Output path for ethogram PNG")
    parser.add_argument("--matrix", default="transition_matrix.png", help="Output path for transition matrix PNG")
    parser.add_argument("--window", type=int, default=10, help="Rolling mean window size (frames)")
    parser.add_argument("--bout", type=float, default=0.3, help="Minimum bout duration (seconds)")
    
    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return 1
        
    try:
        # 1. Load
        print(f"Loading data from {parsed_args.input}...")
        raw_data = load_tracking_data(parsed_args.input)
        
        # 2. Kinematics
        print("Computing kinematics...")
        kinematics = calculate_kinematics(raw_data, window_size=parsed_args.window)
        
        # 3. Classify
        print("Classifying behavioral states...")
        states = classify_behavior(kinematics, sampling_rate=30.0, bout_duration=parsed_args.bout)
        
        # 4. Visualize
        print(f"Generating visualizations: {parsed_args.ethogram}, {parsed_args.matrix}...")
        timestamps = [row['t'] for row in kinematics]
        generate_ethogram(states, timestamps, parsed_args.ethogram)
        generate_transition_matrix(states, parsed_args.matrix)
        
        # 5. Report
        print(f"Generating summary report: {parsed_args.report}...")
        stats = generate_summary_report(kinematics, states, parsed_args.report)
        
        # Final Output / Warnings
        print("\nAnalysis Complete.")
        print(f"Total distance: {stats['total_distance']:.2f} cm")
        if stats['outlier_count'] > 0:
            print(f"WARNING: Outliers detected ({stats['outlier_count']} instances). Please check the report for details.")
            
        return 0
        
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
