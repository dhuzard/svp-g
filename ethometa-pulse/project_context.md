# Project Context: EthoMeta-Pulse

## Goal
Create a Python tool that imports CSV tracking data (t, x, y), computes instantaneous velocity and acceleration, and classifies behavior into three states: 'Stationary', 'Exploration', and 'Rapid Movement'.

## Requirements
1. Use a configurable rolling mean for jitter reduction.
2. Generate an Ethogram plot (time-series of states).
3. Generate a Transition Probability Matrix (Heatmap).

## Stakeholder Context
- Domain: Behavioral Neuroscience
- Role: Domain Expert
- Key Focus Areas for Dialog: sampling rates, coordinate units, state-transition logic.
