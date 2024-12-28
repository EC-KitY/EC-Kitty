# Individual
Abstract class representing a single individual.

## Concrete Individual classes
### Tree
Subclass of Individual, used for GP experiments. \
Tree is represented by a list of TreeNodes. Each node is either a function (inner node) or a terminal (leaf node). Tree nodes are in stored in prefix order.

For instance, the function x*(y+1) is represented as:
```python
[FunctionNode(f_mul), TerminalNode('x'), FunctionNode(f_add), TerminalNode('y'), TerminalNode(1)]
```

The possible nodes of a tree are defined by the fields `function_set` and `terminal_set`.

Casting a Tree to str generates a python function that represents the tree:
```python
>>> from eckity.genetic_encodings.gp import Tree, TerminalNode, FunctionNode
>>> from eckity.base.untyped_functions import f_mul, f_add
>>> t1 = Tree([FunctionNode(f_mul), TerminalNode('x'), FunctionNode(f_add), TerminalNode('y'), TerminalNode(1)], terminal_set=['x', 'y'], function_set=[f_mul, f_add])
>>> print(str(t1))
def func_3(x, y):
  return f_mul(
    x,
    f_add(
      y,
      1
    )
  )
```

### Vector
Subclass of Individual, used for GP experiments.
The genotype is kept in the `vector` field.
The type of the list is homogenous and defined by the concrete vector class:

#### BitStringVector
Binary vector.

#### IntVector
Integer vector.

#### FloatVector
Float vector.
