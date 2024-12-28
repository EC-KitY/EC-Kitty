# Breeder

The Breeder is responsible for the parent selection and the execution of genetic operators (crossover, mutation) in each generation.

We focus on SimpleBreeder, that assumes there is only one Subpopulation.

## General flow

SimpleBreeder first selects all the parents from the population of the previous generation, then applies the genetic operators (crossover, mutation) in a pipeline manner.

For example, suppose we defined the operator sequence as following:
```python
operators_sequence=[
    SubtreeCrossover(probability=0.8, arity=2),
    SubtreeMutation(probability=0.1, arity=1),
]
```

We defined a SubtreeCrossover that operates on two parents with a probability of 0.8 in each generation, and a SubtreeMutation that operators on a single individual at once with a probability of 0.1.
Note that the probabilities don't need to sum to one, as the execution of each operator is independent.

The breeder will iterate over the whole population to apply SubtreeCrossover on pairs of individuals, and only then iterate again over the whole population and attempt to apply the mutation on each individual.

## Advanced - Implementation details
During the design and implementation of SimpleBreeder, we have made several choices that impact its logic:

- The size of the offspring created in each genetic operator **must** be equal to the amount of parents sent to the operator.
For instance, a subtree crossover performed between 2 GP trees must return 2 offspring.

- When applying the genetic operators, SimpleBreeder iterates over the individuals by their selection order, and applies the operators according to their arity. For instance, when applying a SubtreeCrossover that receives two parents, the breeder will first apply the crossover on the first and second individual, then apply the crossover on the third and fourth individual an so on.

If you wish to change this logic, create a new Breeder subclass with your desired logic, submit a PR in our GitHub repository and we will consider including it in the package.
