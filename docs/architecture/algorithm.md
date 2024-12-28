# Algorithm

Evolutionary Algorithm defined in the experiment.
An algorithm can operate on a single Subpopulation, or multiple Subpopulations (coevolution, island model).

The following psuedocode demonstrates the main flow of the algorithm:

```
1. create initial population
2. while termination condition not met do:
    a. evaluate the fitness functions of the current generation
    b. select parents from the current generation
    c. perform crossover and mutation operators
```

Each step is performed by an object that is invoked by the algorithm:
- The creation of the initial population is done by the *Creator*.
- The termination condition check is done by the *TerminationChecker*.
- The fitness evaluation of the population is done by the *Evaluator*.
- The selection, crossover and mutation is done by the *Breeder*.

## Algorithm types

Algorithm is an abstract class.
The most straightforward concrete Algorithm class is *SimpleEvolution*.
SimpleEvolution assumes there is only one population in the evolutionary experiment.
Another Algorithm subclass is *NSGA2Evolution*, used for multi-objective evolution (MOE).

