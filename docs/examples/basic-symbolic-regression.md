# Symbolic Regression (basic mode)

## Preview
In this example we will solve the Symbolic regression problem using our library.

## Setting the experiment
First, we need to import the components we want to use in our experiment.

```python
from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.gp_creators.ramped_hh import RampedHalfAndHalfCreator
from eckity.genetic_encodings.gp.tree.functions import f_add, f_mul, f_sub, f_div, \
    f_sqrt, f_log, f_abs, f_max, f_min, f_inv, f_neg
from eckity.genetic_operators.crossovers.subtree_crossover import SubtreeCrossover
from eckity.genetic_operators.mutations.erc_mutation import ERCMutation
from eckity.genetic_operators.mutations.subtree_mutation import SubtreeMutation
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation
from eckity.termination_checkers.threshold_from_target_termination_checker import ThresholdFromTargetTerminationChecker
from examples.treegp.non_sklearn_mode.symbolic_regression.sym_reg_evaluator import SymbolicRegressionEvaluator
```

Now we can create our experiment. First we define the **function set** and the **terminal set**.
The function set is the set of all possible inner nodes of the tree, and the terminal set is the set of all the leaves in the tree.

### Creating the set of tree nodes
```python
# each node of the GP tree is either a terminal or a function
# function nodes, each has two children (which are its operands)
function_set = [f_add, f_mul, f_sub, f_div, f_sqrt, f_log, f_abs, f_max, f_min, f_inv, f_neg]

# terminal set, consisted of variables and constants
terminal_set = ['x', 'y', 'z', 0, 1, -1]
```

Our tree individuals will contain some common mathematical functions as internal nodes (function set)
and its leaves (terminal set) will be the vars x, y, z, or the constant numbers 0, 1 or -1.

An example of two possible individuals:

![image](https://user-images.githubusercontent.com/62753120/163423348-a60abee0-f1c5-4de7-a63c-a7e6807bc859.png)

## Initializing the evolutionary algorithm
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
                          ERCMutation(probability=0.05, arity=1)
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

## Initializing Subpopulation
Sub-population is the object that holds the individuals, and the objects that are
responsible for treating them (a Population can include a list of multiple
Subpopulations but it is not needed in this case).

### Creating individuals
Here we determined the parameters for the creation of the individuals. We have chosen to
create ramped half and half trees with init depth of 2 to 4, we set the
tree nodes' sets to be the ones we created before, we added bloat values in order to
slow down the trees growth, and we chose our population to contain 200 individuals.
```python
Subpopulation(creators=RampedHalfAndHalfCreator(init_depth=(2, 4),
                                                terminal_set=terminal_set,
                                                function_set=function_set,
                                                bloat_weight=0.0001),
              population_size=200,
```

### Evaluating individuals
Next we set the parameters for evaluating the individuals. We will elaborate on this
later on.

```python
              # user-defined fitness evaluation method
              evaluator=SymbolicRegressionEvaluator(),
              higher_is_better=False,
```

### Breeding process
Now we will set the (hyper)parameters for the breeding process. We chose an elitism rate that determines what percent of the population's top individuals 
will be copied as-is to the next generation in each generation.

Then, we defined genetic operators to be applied in each generation:
* Subtree Crossover with a probability of 90%
* Subtree Mutation with a probability of 20%
* ERC Mutation with a probability of 5% (probabilities don't sum to 1 since operators are simply applied sequentially, in a pipeline manner)
* Tournament Selection with a probability of 1 and with tournament size of 4

```python
              elitism_rate=0.05,
              # genetic operators sequence to be applied in each generation
              operators_sequence=[
                  SubtreeCrossover(probability=0.9, arity=2),
                  SubtreeMutation(probability=0.2, arity=1),
                  ERCMutation(probability=0.05, arity=1)],
              selection_methods=[
                  # (selection method, selection probability) tuple
                  (TournamentSelection(tournament_size=4, higher_is_better=False), 1)]
              )
```

We define our breeder to be the standard simple Breeder (appropriate for the simple case of a single sub-population),
and our max number of worker nodes to compute the fitness values is 4.

```python
        breeder=SimpleBreeder(),
        max_workers=4,
```

### Termination condition and statistics
We define max number of generations (iterations).
The Algorithm may terminate early upon reaching fitness value such that:

`|current fitness - optimal_fitness| <= threshold`
```python
        max_generation=500,
        # random_seed=0,
        termination_checker=ThresholdFromTargetTerminationChecker(optimal=0, threshold=0.001),
        statistics=BestAverageWorstStatistics()
    )
```

Finally, we set our statistics to be the default form of best-average-worst
statistics, which prints the next format in each generation of the evolutionary run:

```
generation #(generation number)
subpopulation #(subpopulation number)
best fitness (some fitness which is the best)
worst fitness (some fitness which is average)
average fitness (some fitness which is just the worst)
```

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
# execute the best individual after the evolutionary process ends, by assigning numeric values to the variable
# terminals in the tree
print(f'algo.execute(x=2,y=3,z=4): {algo.execute(x=2, y=3, z=4)}')
```

# The Symbolic Regression Evaluator
This is where the magic happens, the Evaluator is the object that evaluates the individual fitness,
so here we will choose the direction towards which evolution will progress.

## Target function
In our example we would like our individual to be as close as possible to a function, here 
defined as:

```python
def _target_func(x, y, z):
    """
    True regression function, the individuals
    Parameters
    ----------
    x, y, z: float
        Values to the parameters of the function.
    return x + 2 * y + 3 * z
```

## The Evaluator
We extend the SimpleIndividualEvaluator, which means we will have to implement the evaluate_individual.
We further create a DataFrame with 200 rows for the x, y, z parameters and the target function value:

```python
class SymbolicRegressionEvaluator(SimpleIndividualEvaluator):
    """
    Compute the fitness of an individual.
    """

    def __init__(self):
        super().__init__()

        # np.random.seed(0)

        data = np.random.uniform(-100, 100, size=(200, 3))
        self.df = pd.DataFrame(data, columns=['x', 'y', 'z'])
        self.df['target'] = _target_func(self.df['x'], self.df['y'], self.df['z'])
```

## Evaluating Individuals
When defining an Evaluator for a certain problem, we must implement the `evaluate_individual` method, which evaluates a fitness score for an individual.

We measure how close an individual is to the target function by calculating the mean absolute error between
the target function score (_self.df[target]_) and the individual score (_individual.execute(x=x, y=y, z=z)_)
on the same data frame we defined above.

The _individual.execute_ function runs the tree recursively with the given parameters, which in our example
will return the individual function result.

```python
    def evaluate_individual(self, individual):
        x, y, z = self.df['x'], self.df['y'], self.df['z']
        return np.mean(np.abs(individual.execute(x=x, y=y, z=z) - self.df['target']))
```
