# Genetic Operators
GeneticOperator is a subclass of Operator, additionally including a probability that the operator will apply.

The exact amount of required parents (and returned offspring) is determined by the `arity` field.

Note that genetic operators are performed **in place**, altering the representation of the individuals without copying them.

## Crossover

Crossover is performed during the breeding process and combines the genotype of several individuals **in-place**.

# Mutation

Mutation is performed during the breeding process and independently alters the genotype of one or more individuals **in-place**.
