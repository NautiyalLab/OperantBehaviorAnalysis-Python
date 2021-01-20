# OperantBehaviorAnalysis-Python
This repository will be used in the Nautiyal Lab for analyzing output from MEDAssociates Operant Chambers. 

## Background
Operant conditioning is a form of learning that occurs through responses to behavior. For example, a mouse pushes a lever and then receives a reward. The action of pushing the lever becomes associated with the reward, and the mouse continues the behavior. In out lab, we use operant (as well as Pavlovian) conditioning to examine different aspects of impulsivity. Stephanie has created an excellent codebase for analyzing data produced by MED boxes. 

## Problem
To make the code user friendly, it was primarily written to be used with a GUI. I'd prefer to run it from a CLI, but there are certain aspects now that do not function
well with thiss.
I also prefer to have the ability to automatically  generate graphs of data during training to easily check up on animal progress on a day to day basis. 

## Solution
I'm going to make tweaks that are almost entirely for my own ease of use in this branch. Those tweaks will primarily be resolving any bugs that arise from attempting
to execute certain things from the command line and adding in some graphing functionality. 

## Paradigms and Schedules
### Trough Train (1 and 2)
- In TT1, dipper comes up randomly and remains until reward is retrieved
- In TT2, dipper comes up randomly and remains up for a short time
- measures needed: total dippers, dippers retrieved, latency to retrieve dipper
### Continuous Reinforcement Schedule (CRF)
- Lever(s) come out, all presses are rewarded
- In CRF training, after 2 lever presses, levers go back in, and then come out again after an ITI
- measures needed: total head pokes, total dippers, dippers retrieved, latency to retrieve dipper, total lever presses, latency to press after lever presentation (meaningful)
### Random Ratio
- Lever(s) come out, animal must press lever random number of times (this averages to a specified number) to receive reward
- measures needed: total dippers, dippers retrieved, latency to retrieve dipper, total lever presses
### Random Interval (possibly could use RR script)
- Lever(s) come out, first lever press after a random ITI (this averages to a specified time) receives a reward
- Also known as Variable Interval
- measures needed: total dippers, dippers retrieved, latency to retrieve dipper, total lever presses
### Operant Sensation Seeking
- Levers come out, all presses on the "active" lever are rewarded with a combination of stimuli (white noise and blinking lights at varying frequency, for a variable time interval)
- For control group, no lever presses are rewarded
- measures needed: total active and inactive lever presses
### Conditioned Inhibition
- measures needed: rate of responding during each cue type, responding during an equivalent portion of the ITI preceeding the cue, elevation score 
#### Training
- In experimental animals, cue 1 is followed by reward, cue 2 is followed by reward, cue 1/cue 3 is not rewarded
- In control animals, cue 1 is followed by reward, cue 2 is followed by reward, cue 3 is not rewarded
#### Summation
- Cue 2 is followed by reward, cue 2/cue 3 is not rewarded
- additional measure needed: 
#### Retardation
- Cue 3 is followed by reward
### Pavlovian Cue Elicited Responding
- Cue presentation is followed by reward
- measures needed: total dippers, dippers retrieved, latency to retrieve dipper, response rate and duration during cue (each binned by seconds), overall response rate during cue/equivalent portion of the ITI preceeding the cue
#### PCER with Unrewarded Trials
- Random cue trials are not rewarded
- additional measure needed: response rate and duration during unrewarded "wait period" following cue (each binned by seconds) 
### Go/No-Go
- During go trials, lever press is rewarded
- During no-go trials, withholding lever pressing is rewarded
- measures needed: total head pokes, total dippers, dippers retrieved, latency to retrieve dipper, total lever presses, number of go/no-go trials, latency to push lever during go/no-go trials, number of successful go/no-go trials, overall latency to press after lever presentation (meaningful)
### Progressive Ratio
- Each subsequent reward requires more lever pressing
- For example in PRx2, 1 press is needed for reward, then 2, 4, 8, 16, etc
- measures needed: total head pokes, total dippers, dippers retrieved, latency to retrieve dipper, total lever presses, breakpoint
### Differential Reinforcement of Low Rate Responding
- Animals must withhold lever presses until after a wait period is over to be rewarded
- If they resond early, the wait period starts over
- measures needed: total head pokes, total dippers, dippers retrieved, latency to retrieve dipper, total lever presses, lever to dipper ratio, peak mode latencies, histogram of lever press latencies (binned by 3 seconds)
### Habit
- Current testing schedule: VI30 (3 days), VI60 (3/6/9 days), Extinction, Reaquisition (VI60), Devaluation, Extinction 2, Reaquisition 2 (VI60) 
#### Training
- Trained using a random interval schedule
- measures needed: total dippers, dippers retrieved, latency to retrieve dipper, total lever presses
#### Extinction
- Lever presses are not rewarded (15 minutes total)
- measures needed: total lever presses, rate of lever pressing (binned by 5 minutes)
#### Reaquisition
- Random interval schedule again
- measures needed: total dippers, dippers retrieved, latency to retrieve dipper, total lever presses, rate of lever pressing (binned by 5 minutes)
#### Devaluation
- Animals receive randomly delivered rewards (20 minutes), given LiCl, then placed back in context (20 minutes)
- Reward delivery is the same as TT2, so that analysis can be used here
### Visualization of Session
- I will be adding some of that in the Command Line branch. 
