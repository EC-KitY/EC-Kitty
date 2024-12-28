# Multiplexer

## Preview
In this example we solve the Multiplexer problem with GP, using EC-KitY.

## Setting the experiment
First, we need to import the components we want to use in our experiment.

```python
from time import time

from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.gp_creators.full import FullCreator
from eckity.genetic_encodings.gp.tree.functions import f_and, f_or, f_not, f_if_then_else
from eckity.genetic_operators.crossovers.subtree_crossover import SubtreeCrossover
from eckity.genetic_operators.mutations.subtree_mutation import SubtreeMutation
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation
from eckity.termination_checkers.threshold_from_target_termination_checker import ThresholdFromTargetTerminationChecker
from examples.treegp.non_sklearn_mode.multiplexer.mux_evaluator import MuxEvaluator, NUM_SELECT_ENTRIES, NUM_INPUT_ENTRIES
```
Now we can create our experiment. First we define the **function set** and the **terminal set**.
The function set is the set of all possible inner nodes of the tree, and the terminal set is the set of all the leaves in the tree.

### Creating the set of tree nodes
```python
# The terminal set of the tree will contain the mux inputs (d0-d7 in a 8-3 mux gate),
# 3 select lines (s0-s2 in a 8-3 mux gate) and the constants 0 and 1
select_terminals = [f's{i}' for i in range(NUM_SELECT_ENTRIES)]
input_terminals = [f'd{i}' for i in range(NUM_INPUT_ENTRIES)]
terminal_set = select_terminals + input_terminals + [0, 1]

# Logical functions: and, or, not, and if-then-else
function_set = [f_and, f_or, f_not, f_if_then_else]
```
Our tree individuals will have some common logical functions and its leaves will be the select lines s0-s2, the input lines d0-d7, or the logical constants 0 (False) and 1 (True).

An example for a possible individual representation in this manner:

![image](https://user-images.githubusercontent.com/62753120/163422945-d433b195-9443-4797-90fb-665e181bec80.png)

### Initializing the evolutionary algorithm
The Evolution object is the main part of the experiment. It receives the parameters of
the experiment and runs the evolutionary process:
```python
algo = SimpleEvolution(
        Subpopulation(creators=RampedHalfAndHalfCreator(init_depth=(2, 4),
                                                        terminal_set=terminal_set,
                                                        function_set=function_set,
                                                        bloat_weight=0.0001),
                      population_size=200,
                      # user-defined fitness evaluation method
                      evaluator=SymbolicRegressionEvaluator(),
                      # minimization problem (fitness is MAE), so higher fitness is worse
                      higher_is_better=False,
                      elitism_rate=0.05,
                      # genetic operators sequence to be applied in each generation
                      operators_sequence=[
                          SubtreeCrossover(probability=0.9, arity=2),
                          SubtreeMutation(probability=0.2, arity=1),
                          ErcMutation(probability=0.05, arity=1)
                      ],
                      selection_methods=[
                          # (selection method, selection probability) tuple
                          (TournamentSelection(tournament_size=4, higher_is_better=False), 1)
                      ]
                      ),
        breeder=SimpleBreeder(),
        max_workers=4,
        max_generation=500,
        # random_seed=0,
        termination_checker=ThresholdFromTargetTerminationChecker(optimal=0, threshold=0.001),
        statistics=BestAverageWorstStatistics()
    )
```
Let's break down the parts and understand their meaning.

### Initializing Subpopulation
Sub-population is the object that holds the individuals, and the objects that are
responsible for treating them (a Population can include a list of multiple
Subpopulations but it is not needed in this case).

### Creating individuals
We have chosen to use ramped-half-and-half trees with init depth of 2 to 4. We set the
tree nodes' sets to be the ones we created before, and we added bloat control in order to
limit the tree sizes. Finally, we chose our population to contain 40 individuals.
```python
    algo = SimpleEvolution(
        Subpopulation(creators=FullCreator(init_depth=(2, 4),
                                           terminal_set=terminal_set,
                                           function_set=function_set,
                                           bloat_weight=0.00001),
                      population_size=40,
```

### Evaluating individuals
Next we set the parameters for evaluating the individuals. We will elaborate on this
later on.
```python
              # user-defined fitness evaluation method
              evaluator=MuxEvaluator(),
              higher_is_better=True,
```
### Breeding process
Now we will set the (hyper)parameters for the breeding process. We declared that none of the individuals will be considered as elite.

Then, we defined the genetic operators to be applied in each generation:
* Subtree Crossover with a probability of 80%
* Subtree Mutation with a probability of 10% (probabilities don't sum to 1 since operators are simply applied sequentially, in a pipeline manner)
* Tournament Selection with a probability of 1 and with tournament size of 7

```python
              elitism_rate=0.0,
              # genetic operators sequence to be applied in each generation
              operators_sequence=[
                  SubtreeCrossover(probability=0.8, arity=2),
                  SubtreeMutation(probability=0.1, arity=1)
              ],
              selection_methods=[
                  # (selection method, selection probability) tuple
                  (TournamentSelection(tournament_size=7, higher_is_better=True), 1)
              ]
              ),
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
The Algorithm may terminate early upon reaching fitness value such that:
`|current fitness - optimal_fitness| <= threshold`
```python
        max_generation=40,
        termination_checker=ThresholdFromTargetTerminationChecker(optimal=1, threshold=0.01),
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
After the evolve stage has finished (either by exceeding the maximal number of generations or by reaching a
pre-defined threshold), we can execute the algorithm to check the evolutionary results:
```python
    # execute the best individual after the evolution process ends
    exec1 = algo.execute(s0=0, s1=0, s2=1, d0=0, d1=0, d2=1, d3=1, d4=1, d5=0, d6=0, d7=1)
    exec3 = algo.execute(s0=0, s1=1, s2=1, d0=0, d1=0, d2=1, d3=1, d4=1, d5=0, d6=0, d7=1)
    exec7 = algo.execute(s0=1, s1=1, s2=1, d0=0, d1=0, d2=1, d3=1, d4=1, d5=0, d6=0, d7=1)
    print('execute(s0=0, s1=1, s2=1, d1=0): expected value = 0, actual value =', exec1)
    print('execute(s0=0, s1=0, s2=1, d3=1): expected value = 1, actual value =', exec3)
    print('execute(s0=1, s1=1, s2=1, d7=1): expected value = 1, actual value =', exec7)

    print('total time:', time() - start_time)
```

# The Multiplexer Evaluator

## What is an Evaluator?
Problem-specific fitness evaluation method.

For each problem we need to supply a mechanism to compute an individual's fitness score,
which determines how "good" (fit) this particular individual is.

Let's go through the parts of the Multiplexer problem Evaluator:

Simple version evaluator (SimpleIndividualEvaluator) sub-classes compute fitness scores of each individual separately,
while more complex Individual Evaluators may compute the fitness of several individuals at once.
```python
from itertools import product
from numbers import Number

import pandas as pd
import numpy as np

from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
```

The Multiplexer gate has two type of entries - data entries and select entries.
The select entries determine which data entry should the logical gate choose.

We will use a 8-3 Multiplexer gate example (8 data entries, 3 select entries)

```python
NUM_SELECT_ENTRIES = 3
NUM_INPUT_ENTRIES = 2 ** NUM_SELECT_ENTRIES
NUM_COLUMNS = NUM_SELECT_ENTRIES + NUM_INPUT_ENTRIES
NUM_ROWS = 2 ** NUM_COLUMNS
```

## Target function

The goal of this problem is to obtain an individual GP Tree that acts as a Multiplexer gate, 
i.e., an individual that has the same truth table as a Multiplexer gate.
The target function is basically a function that receives values of data and select entries,
and returns the output according to a Multiplexer gate truth table.

Ideally, a perfect GP Tree execution should be equivalent to the execution of the target function. 

```python
def _target_func(s0, s1, s2, d0, d1, d2, d3, d4, d5, d6, d7):
    """
    Truth table of a 8-3 mux gate

    Returns the value of d_i, where i is the decimal value of the binary number obtained by joining s0, s1 and s2 digits
    (see examples below)

    Parameters
    ----------
    s0-s2: int
        select values for the mux gate

    d0-d7: int
        input values for the mux gate

    Returns
    -------
    int
        0 (False) or 1 (True), depends on the values of the given parameters

    Examples
    -------
    _target_func(s0=0, s1=0, s2=0, d0=1, ...) = 1 (the value of input entry d0)
    _target_func(s0=0, s1=0, s2=1, d0=1, d1=0, ...) = 0 (the value of input entry d1)
    """
    return ((not s0) and (not s1) and (not s2) and d0) \
           or ((not s0) and (not s1) and s2 and d1) \
           or ((not s0) and s1 and (not s2) and d2) \
           or ((not s0) and s1 and s2 and d3) \
           or (s0 and (not s1) and (not s2) and d4) \
           or (s0 and (not s1) and s2 and d5) \
           or (s0 and s1 and (not s2) and d6) \
           or (s0 and s1 and s2 and d7)
```

## Defining the Multiplexer Evaluator
Our evaluator extends the SimpleIndividualEvaluator class, thus computing each individual's fitness separately.

It holds the Multiplexer gate truth table to evaluate how close an individual is to the target function.  
This truth table splits into inputs (all possible combinations of select and data entries) and outputs
(expected Multiplexer gate output for each possible input).
```python
class MuxEvaluator(SimpleIndividualEvaluator):
    """
    Evaluator class for the Multiplexer problem, responsible for defining a fitness evaluation method and evaluating it

    Attributes
    -------
    inputs: pandas DataFrame
        Input columns representing all possible combinations of all select values and input values.

    output: pandas Series
        All possible output values. Values depend on the matching rows from the inputs DataFrame.
    """

    def __init__(self):
        super().__init__()

        # construct a truth table of all combinations of ones and zeros
        values = [list(x) + [_target_func(*x)] for x in product([0, 1], repeat=_target_func.__code__.co_argcount)]
        truth_tbl = pd.DataFrame(values, columns=(list(_target_func.__code__.co_varnames) + ['output']))

        # split dataframe to input columns and an output column
        self.inputs = truth_tbl.iloc[:, :NUM_COLUMNS]
        self.output = truth_tbl['output']
```

## Evaluating Individuals
When defining an Evaluator for a certain problem, we must implement the `evaluate_individual` method, which evaluates a fitness score for an individual.

For a given Individual (specifically in this case, a given GP tree), this Evaluator will execute it
with all possible input combinations, then compare the results to the ideal Multiplexer gate.
The fitness value will be the accuracy score of this comparison, ranging from 0 (all outputs differ) to 1 (exact same outputs).
```python
    def evaluate_individual(self, individual):
        """
        Compute the fitness value of a given individual.

        Fitness evaluation is done by calculating the accuracy through comparison of the tree execution result and the optimal result
        (multiplexer truth table).

        Parameters
        ----------
        individual: Tree
            The individual to compute the fitness value for.

        Returns
        -------
        float
            The evaluated fitness value of the given individual.
            The value ranges from 0 (worst case) to 1 (best case).
        """

        # select entries columns
        s0, s1, s2 = self.inputs['s0'], self.inputs['s1'], self.inputs['s2']
        # input entries columns
        d0, d1, d2, d3, d4, d5, d6, d7 = self.inputs['d0'], self.inputs['d1'], self.inputs['d2'], self.inputs['d0'], \
                                         self.inputs['d4'], self.inputs['d5'], self.inputs['d6'], self.inputs['d7']

        exec_res = individual.execute(s0=s0, s1=s1, s2=s2, d0=d0, d1=d1, d2=d2, d3=d3, d4=d4, d5=d5, d6=d6, d7=d7)

        # sometimes execute will return a single scalar (in cases of constant trees)
        if isinstance(exec_res, Number) or exec_res.shape == np.shape(0):
            exec_res = np.full((NUM_ROWS,), exec_res)

        # The more "matches" the individual's execute result has with expected output,
        # the better the individual's fitness is.
        # Worst Case: the individual returned only wrong (binary) results, and should have a fitness of 0.
        # The bitwise_xor operator will return a vector of ones, which sums to NUM_ROWS, resulting in a fitness of 0.
        # Best case: the individual returned only right (binary) results, and should have a fitness of 1.
        # The bitwise_xor operator will return a vector of zeros, which sums to 0, resulting in a fitness of 1.
        return (NUM_ROWS - np.sum(np.bitwise_xor(exec_res, self.output))) / NUM_ROWS

```
