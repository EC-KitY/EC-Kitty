# Custom Problems

In case you want to solve a problem that does not appear in the Examples folder, you only need to do these two things:
- Choose the individual representation (either from the existing ones in genetic_encodings folder, or a custom representation of your own)
- Define a custom SimpleIndividualEvaluator subclass.

Let's define a new GA problem called zero-max, which is the exact opposite of the one-max problem.
If you are not familiar with the one-max problem, refer to the [One-Max tutorial](../tutorials/one-max.md).

We will use bit-string vectors (as in the original problem).
As for the fitness function, the fitness scores will be the number of zeros in the vector.

```python
from eckity.evaluators import SimpleIndividualEvaluator

class ZeroMaxEvaluator(SimpleIndividualEvaluator):
    def evaluate_individual(individual):
        vector = individual.get_vector()

        # number of zeros is the maximum amount of ones (vector length) minus the actual amount of ones (vector sum)
        return len(vector) - sum(vector)
```

Et voilà! we are ready to use our new evaluator in an evolutionary experiment.

```python
from eckity.algorithms import SimpleEvolution
from eckity.subpopulation import Subpopulation
from eckity.creators import GABitStringVectorCreator
from eckity.genetic_operators import VectorKPointCrossover, BitStringVectorFlipMutation

algo = SimpleEvolution(
    Subpopulation(
        creators=GABitStringVectorCreator(
            length=100,
        ),
        evaluator=ZeroMaxEvaluator(),
        operators_sequence=[
            VectorKPointCrossover(),
            BitStringVectorFlipMutation()
        ]
    )
)

algo.evolve()

# Execute (show) the best solution
print(algo.execute())
```
