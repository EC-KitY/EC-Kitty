# Knapsack

## Preview
In this example we solve the 0-1 Knapsack problem with GA, using EC-KitY.

## Setting the experiment
First, we need to import the components we want to use in our experiment.

```python
from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.ga_creators.bit_string_vector_creator import GABitStringVectorCreator
from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
from eckity.genetic_operators.mutations.vector_random_mutation import BitStringVectorFlipMutation
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation

from examples.vectorga.knapsack.knapsack_evaluator import KnapsackEvaluator, NUM_ITEMS
```
Now we can create our experiment. 

### Initializing the evolutionary algorithm
The Evolution object is the main part of the experiment. It receives the parameters of
the experiment and runs the evolutionary process:
```python
algo = SimpleEvolution(
        Subpopulation(creators=GABitStringVectorCreator(length=NUM_ITEMS),
                      population_size=50,
                      # user-defined fitness evaluation method
                      evaluator=KnapsackEvaluator(),
                      # maximization problem (fitness is sum of values), so higher fitness is better
                      higher_is_better=True,
                      # genetic operators sequence to be applied in each generation
                      operators_sequence=[
                          VectorKPointsCrossover(probability=0.5, k=2),
                          BitStringVectorFlipMutation(probability=0.05)
                      ],
                      selection_methods=[
                          # (selection method, selection probability) tuple
                          (TournamentSelection(tournament_size=4, higher_is_better=True), 1)
                      ]),
        breeder=SimpleBreeder(),
        max_workers=1,
        max_generation=500,
        statistics=BestAverageWorstStatistics()
    )
```
Let's break down the parts and understand their meaning.

### Initializing Subpopulation
Sub-population is the object that holds the individuals, and the objects that are
responsible for treating them (a Population can include a list of multiple
Subpopulations but it is not needed in this case).

### Creating individuals
We have chosen to use bit vectors with a length equal to the number of the items in the pool. Moreover, we chose our population to contain 50 individuals.
```python
algo = SimpleEvolution(
        Subpopulation(creators=GABitStringVectorCreator(length=NUM_ITEMS),
                      population_size=50,
```

### Evaluating individuals
Next we set the parameters for evaluating the individuals. We will elaborate on this
later on.
```python
                      # user-defined fitness evaluation method
                      evaluator=KnapsackEvaluator(),
                      # maximization problem (fitness is sum of values), so higher fitness is better
                      higher_is_better=True,
```
### Breeding process
Now we will set the (hyper)parameters for the breeding process. We declared that none of the individuals will be considered as elite.

Then, we defined the genetic operators to be applied in each generation:
* 2 Point Crossover with a probability of 50%
* Bit Flip Mutation with a probability of 5% (probabilities don't sum to 1 since operators are simply applied sequentially, in a pipeline manner)
* Tournament Selection with a probability of 1 and with tournament size of 4

```python
                      elitism_rate=0.0,
                      # genetic operators sequence to be applied in each generation
                      operators_sequence=[
                          VectorKPointsCrossover(probability=0.5, k=2),
                          BitStringVectorFlipMutation(probability=0.05)
                      ],
                      selection_methods=[
                          # (selection method, selection probability) tuple
                          (TournamentSelection(tournament_size=4, higher_is_better=True), 1)
                      ]),
```
Now that we are done with our Subpopulation, we will finish setting the evolutionary algorithm.

We define our breeder to be the standard simple Breeder (appropriate for the simple case of a single sub-population),
and our max number of worker nodes to compute the fitness values is 1.
```python
        breeder=SimpleBreeder(),
        max_workers=1,
```
### Termination condition and statistics
We define max number of generations (iterations).
Unlike other examples, we didn't define a `TerminationChecker` (early termination mechanism) in this example, since the items are generated randomly and thus the optimal value is also random.
```python
        max_generation=500,
        statistics=BestAverageWorstStatistics(),
    )
```
Finally, we set our statistics to be the default form of best-average-worst
statistics which prints the next format in each generation of the evolutionary run:
```
generation #(generation number)
subpopulation #(subpopulation number)
best fitness (some fitness which is the best)
worst fitness (some fitness which is average)
average fitness (some fitness which is just the worst)
```

Another possible keyword argument to the program is a seed value. This enables to replicate results across different runs
with the same parameters.

## Evolution stage
After setting up the evolutionary algorithm, we can finally begin the run:
```python
    # evolve the generated initial population
    algo.evolve()
```

## Execution stage
After the evolve stage has finished (by exceeding the maximal number of generations), we can execute the Algorithm and show the best-of-run vector (solution) to check the evolutionary results:
```python
    # Execute (show) the best solution
    print(algo.execute())
```

# The Knapsack Evaluator

## What is an Evaluator?
Problem-specific fitness evaluation method.

For each problem we need to supply a mechanism to compute an individual's fitness score,
which determines how "good" (fit) this particular individual is.

Let's go through the parts of the Knapsack problem Evaluator:

Simple version evaluator (SimpleIndividualEvaluator) sub-classes compute fitness scores of each individual separately,
while more complex Individual Evaluators may compute the fitness of several individuals at once.
```python
import random
import numpy as np

from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
```

We will declare the number of items to be 20 by default
```python
NUM_ITEMS = 20
```

## Defining the Knapsack Evaluator
Our evaluator extends the SimpleIndividualEvaluator class, thus computing each individual's fitness separately.
This evaluator keeps the collection of the possible items, and the maximal weight of the bag.

```python
class KnapsackEvaluator(SimpleIndividualEvaluator):
    """
    Evaluator class for the Knapsack problem, responsible of defining a fitness evaluation method and evaluating it.
    In this example, fitness is the total price of the knapsack

    Attributes
    -------
    items: dict(int, tuple(int, float))
        dictionary of (item id: (weights, prices)) of the items
    """

    def __init__(self, items=None, max_weight=30):
        super().__init__()

        if items is None:
            # Generate ramdom items for the problem (keys=weights, values=values)
            items = {i: (random.randint(1, 10), random.uniform(0, 100)) for i in range(NUM_ITEMS)}
        self.items = items
        self.max_weight = max_weight
```

## Evaluating Individuals
When defining an Evaluator for a certain problem, we must implement the `evaluate_individual` method, which evaluates a fitness score for an individual.

For a given Individual (specifically in this case, a given GA vector), this Evaluator will compute the total value of the items
in the bag.
The fitness value will be the computed total value if the total weights of the items does not exceed `max_weight`, and minus infinity if it does exceed `max_weight`.
```python
    def evaluate_individual(self, individual):
        """
        Compute the fitness value of a given individual.

        Parameters
        ----------
        individual: Vector
            The individual to compute the fitness value for.

        Returns
        -------
        float
            The evaluated fitness value of the given individual.
        """
        weight, value = 0.0, 0.0
        for i in range(individual.size()):
            if individual.cell_value(i):
                weight += self.items[i][0]
                value += self.items[i][1]

        # worse possible fitness is returned if the weight of the items exceeds the maximum weight of the bag
        if weight > self.max_weight:
            return -np.inf

        # fitness value is the total value of the bag
        return value
```