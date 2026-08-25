# Smart Factory Local Experiments

## Requirements

The following arch linux packages:
1. **Vagrant**: version 2.4.9-1
2. **VirtualBox**: version 7.2.14-1
3. **Python**: version 3.14.6-1

## Structure

* `src`: Directory containing the code for all the performed experiments
* `src/Metric{x}`: Directory containing the code for experiments performed for metric *x*
* `src/Metric{x}/Experiment{y}` : Directory containing the code for experiment *y* of metric *x*
* `src/Metric{x}/Experiment{y}/CSM` : Directory containing the setup code for CSM experiments
* `src/Metric{x}/Experiment{y}/Dapr` : Directory containing the setup code for Dapr experiments
* `results/Metric{x}/Experiment{y}/Cirrina` : Directory containing the Cirrina (CSM) results for the given experiment
* `results/Metric{x}/Experiment{y}/Dapr` : Directory containing the Dapr results for the given experiment

## Instructions

Generate .jar files for the service, metrics collector and event publisher and add to the appropriate docker folder in `results/Metric{x}/Experiment{y}/Cirrina` and `results/Metric{x}/Experiment{y}/Dapr`.

Each experiment has as `run.py` file which orchestrates and executes the experiments. Execute the file using python.
