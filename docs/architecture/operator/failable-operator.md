# Failable Operator
Some genetic operators might fail sometimes.
For instance, a mutation that results in an illegal offspring.

These operators should inherit from FailableOperator. This class includes an attempt mechanism (`attempt_operator`), and a failing mechanism (`on_fail`).

Failable operators integrated in EC-KitY:[FloatVectorGaussOnePointMutation](https://github.com/EC-KitY/EC-KitY/blob/main/eckity/genetic_operators/mutations/vector_n_point_mutation.py) and [SubtreeMutation (failable in typed GP)](https://github.com/EC-KitY/EC-KitY/blob/main/eckity/genetic_operators/mutations/subtree_mutation.py).
