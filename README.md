# OperantParadigmAnalysis-Python
This repository will contain python scripts for analyzing output from MEDAssociates Operant Chambers. 

## Problem
I (Stephanie) will be rewriting analysis code that I wrote (self-taught, so full of anti-patterns and inefficient) in MatLab. Analysis for Nautiyal Lab operant data used to be done in Excel macros, which was time consuming, convoluted, and inflexible. Ideally this code will be accessible, so everyone in our lab will be able to use and modify it as needed. The code needs to be usable for people with very little programming experience.
The operant boxes simply output a list of numbers, which are concatenated time and event codes (when something happened, and what happened). We need code which will read these files, separate time and event codes, and derive meaningful behavioral analysis. 
Also, we need the code to be flexible, so we can input a single day's run of animals on that day for immediate feedback, but also input multiple days at once do we can see changes over time. 

## Solution
The ultimate solution to this problem is to write scripts for each kind of paradigm we use in the lab, where the user inputs files, subject numbers, and conditions, and the program outputs behavioral measures in tables or graphs as needed.
The first goal will be to write scripts for each operant paradigm, which will analyze a single animal's run in the operant box.
The second goal will be to extend the scripts to analyze multiple animals across days.
The final goal will be to graph the computed analysis.

## Paradigms
#### Trough Train (1 and 2)
#### Continuous Reinforcement Schedule (CRF)
#### Random Ratio and Random Interval (possibly could use CRF script)
#### Operant Sensation Seeking
#### Conditioned Inhibition
#### Pavlovian Cue Elicited Responding
#### Go/No-Go
#### Progressive Ratio
#### Differential Reinforcement of Low Rate 
#### Visualization of Session
