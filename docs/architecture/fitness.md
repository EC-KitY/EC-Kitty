# Fitness
Each individual holds an instance of a Fitness class, which is responsible of maintaining the fitness state of the individual (whether it was already evaluated, the fitness value etc.).

Fitness is an abstract class, with its most frequent subclass being `SimpleFitness`.

## SimpleFitness
Assumes each individual has its own fitness score, and that it is independent from the fitness scores of other individuals.

Contains a float fitness field.

## GPFitness
Extends `SimpleFitness` with an addition of a float `bloat_weight` parameter.

Since bigger trees might cause a significant slow-down of the algorithm, we add a small punishment to the fitness function, based on the size of the tree.
The augmented fitness value is calculated as:
```
augmented_fitness = bloat_weight * tree_size + (1-bloat_weight) * pure_fitness
```

Where pure_fitness is the original fitness value of the tree (regardless of its size).
