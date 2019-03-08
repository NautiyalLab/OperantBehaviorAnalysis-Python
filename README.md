# OperantBehaviorAnalysis-Python
This repository will contain python scripts for analyzing output from MEDAssociates Operant Chambers. 

## Background
Operant conditioning is a form of learning that occurs through responses to behavior. For example, a mouse pushes a lever and then receives a reward. The action of pushing the lever becomes associated with the reward, and the mouse continues the behavior. In out lab, we use operant conditioning (as well as other learning paradigms, like Pavlovian) to test aspects of impulsivity.

## Problem
I (Stephanie) will be rewriting analysis code that I wrote (self-taught, so full of anti-patterns and inefficient) in MatLab. Analysis for Nautiyal Lab operant data used to be done in Excel macros, which was time consuming, convoluted, and inflexible. Ideally this code will be accessible, so everyone in our lab will be able to use and modify it as needed. The code needs to be usable for people with very little programming experience.
The operant boxes simply output a list of numbers, which are concatenated time and event codes (for example, 160901011.0, where 16090 is a relative time and 1011 indicates that the mouse broke an IR beam, poking their head into the reward receptacle). These numbers are outputed everytime something happens, both the in mouse's behavior and in the operant box (like lights going on or levers coming out). We need code which will read these files, separate time and event codes, and derive meaningful behavioral analysis. 
Also, we need the code to be flexible, so we can input a single day's run of animals on that day for immediate feedback, but also input multiple days at once so we can see changes over time. 

## Solution
The ultimate solution to this problem is to write scripts for each kind of paradigm we use in the lab, where the user inputs files (or folders for each day) and conditions, and the program outputs behavioral measures in tables or graphs as needed.
The first goal will be to write functions for each operant paradigm, which will analyze a single animal's run in the operant box.
The second goal will be to write scripts to analyze multiple animals across days.
The final goal will be to graph the computed analysis.

## Paradigms and Schedules
#### Trough Train (1 and 2)
- In TT1, dipper comes up randomly and remains until reward is retrieved
- In TT2, dipper comes up randomly and remains up for a short time
- measures needed: total dippers, dippers retrieved, latency to retrieve dipper
#### Continuous Reinforcement Schedule (CRF)
- Lever(s) come out, all presses are rewarded
- measures needed: total head pokes, total dippers, dippers retrieved, latency to retrieve dipper, total lever presses, latency to press after lever presentation (meaningful)
#### Random Ratio
- Lever(s) come out, animal must press lever random number of times (this averages to a specified number) to receive reward
- measures needed: total dippers, dippers retrieved, latency to retrieve dipper, total lever presses
#### Random Interval (possibly could use RR script)
- Lever(s) come out, first lever press after a random ITI (this averages to a specified time) receives a reward
- measures needed: total dippers, dippers retrieved, latency to retrieve dipper, total lever presses
#### Operant Sensation Seeking
- Levers come out, all presses on the "active" lever are rewarded with a combination of stimuli (white noise and blinking lights at varying frequency, for a variable time interval)
- For control group, no lever presses are rewarded
- measures needed: total active and inactive lever presses
#### Conditioned Inhibition
- measures needed: rate of responding during each cue type, responding during an equivalent portion of the ITI preceeding the cue, elevation score 
##### Training
##### Summation
-additional measure needed: 
##### Retardation
#### Pavlovian Cue Elicited Responding
- measures needed: total dippers, dippers retrieved, latency to retrieve dipper, response rate and duration during cue (each binned by seconds), overall response rate during cue/equivalent portion of the ITI preceeding the cue
##### PCER with Unrewarded Trials
-additional measure needed: response rate and duration during unrewarded "wait period" following cue (each binned by seconds) 
#### Go/No-Go
- measures needed: total head pokes, total dippers, dippers retrieved, latency to retrieve dipper, total lever presses, number of go/no-go trials, latency to push lever during go/no-go trials, number of successful go/no-go trials, overall latency to press after lever presentation (meaningful)
#### Progressive Ratio
- measures needed: total head pokes, total dippers, dippers retrieved, latency to retrieve dipper, total lever presses, breakpoint
#### Differential Reinforcement of Low Rate Responding
- measures needed: total head pokes, total dippers, dippers retrieved, latency to retrieve dipper, total lever presses, lever to dipper ratio, peak mode latencies, histogram of lever press latencies (binned by 3 seconds)
#### Habit
##### Training
##### Extinction
##### Reaquisition
##### Devaluation
#### Visualization of Session
