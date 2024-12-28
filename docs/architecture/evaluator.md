# Evaluator

The Evaluator is responsible for computing the fitness values of the individuals in the experiment.

There are two types of evaluators:
1) PopulationEvaluator
2) IndividualEvaluator

## Population Evaluator

Responsible of computing fitness in population-level.

Currently, the only concrete PopulationEvaluator subclass is `SimplePopulationEvaluator`, that assumes fitness scores of distinct individuals are independent.

## Individual Evaluator
Responsible of computing the fitness value of a single individual.

Currently, the only concrete IndividualEvaluator subclass is `SimpleIndividualEvaluator`, that computes the fitness score of each individual independently.

`SimpleIndividualEvaluator` defines an abstract `evaluate_individual` method. This method receives a single individual and returns a float value representing its fitness score.

Each Evolutionary Computation problem should have a dedicated SimpleIndividualEvaluator subclass that will compute the specific fitness function of the problem.
