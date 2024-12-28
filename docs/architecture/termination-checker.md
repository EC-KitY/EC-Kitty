# Termination Checker

`TerminationChecker` is activated once every generation, and determines whether the algorithm should perform early termination based on a predefined condition.

`TerminationChecker` defines an abstract method `should_terminate` that must be implemented in subclasses.

## ThresholdFromTargetTerminationChecker
The most common `TerminationChecker` instance is [ThresholdFromTargetTerminationChecker](https://github.com/EC-KitY/EC-KitY/blob/develop/eckity/termination_checkers/threshold_from_target_termination_checker.py).
This object is instantiated with an optimal fitness target value and a desired threshold, and signals the algorithm to terminate when distance between the current best fitness value and the optimal fitness is smaller than the predefined threshold.
