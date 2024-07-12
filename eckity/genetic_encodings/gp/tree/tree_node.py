import numpy as np
from abc import ABC, abstractmethod
from numbers import Number
from types import NoneType
from typing import Any, Callable, Dict, List, Optional, get_type_hints

from overrides import override

from eckity.base.utils import arity


class TreeNode(ABC):
    """
    GP Node

    Attributes
    ----------
    node_type : type
        node type
    """

    def __init__(
        self, node_type: Optional[type] = NoneType, parent: "TreeNode" = None
    ) -> None:
        self.node_type = node_type
        self.parent = parent

    @abstractmethod
    def execute(self, **kwargs):
        """
        Returns the value of this node
        Return type must match the type of this node
        """
        pass

    @abstractmethod
    def depth(self):
        """Recursively compute depth"""
        pass

    @abstractmethod
    def generate_tree_code(self, prefix, result):
        """Recursively produce a simple textual printout of the tree"""
        pass

    def __eq__(self, other):
        return (
            isinstance(other, TreeNode) and self.node_type == other.node_type
        )

    def replace_child(self, old_child, new_child):
        pass

    def size(self):
        return 1

    def filter_nodes(
        self, filter_func: Callable, nodes: List["TreeNode"]
    ) -> None:
        if filter_func(self):
            nodes.append(self)


class FunctionNode(TreeNode):
    def __init__(
        self,
        function: Callable,
        children: List[TreeNode] = None,
        parent: TreeNode = None,
    ) -> None:
        # infer the return type of the function
        func_types = FunctionNode.get_func_types(function)
        return_type = func_types[-1] if func_types else NoneType

        if 0 < len(func_types) < arity(function) + 1:
            raise ValueError(
                f"Function {function.__name__} has missing type hints."
                f"Please provide type hints for all arguments and return type."
            )

        super().__init__(return_type, parent)

        self.function = function
        self.n_children = arity(function)

        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    @override
    def execute(self, **kwargs):
        """
        Recursively execute the tree by traversing it in a depth-first order
        """

        arglist = []
        for child in self.children:
            res = child.execute(**kwargs)
            arglist.append(res)
        return self.function(*arglist)

    def add_child(self, child: TreeNode) -> None:

        child_idx = len(self.children)

        # Check if there are too many children
        if child_idx >= arity(self.function):
            raise ValueError(
                f"Too many children for function {self.function}."
            )

        # Check if child is of the correct type
        func_types = FunctionNode.get_func_types(self.function)

        # Check if the child is of the correct type
        expected_type = func_types[child_idx]
        if not issubclass(child.node_type, expected_type):
            raise TypeError(
                f"Expected Child {child_idx} of function "
                f"{self.function.__name__} to be subtype of {expected_type}."
                f"Got {child.node_type}."
            )

        self.children.append(child)

    @override
    def depth(self):
        """Recursively compute depth"""
        return 1 + max([child.depth() for child in self.children], default=0)

    @override
    def size(self):
        return 1 + sum([child.size() for child in self.children])

    @override
    def generate_tree_code(self, prefix, result):
        """Recursively produce a simple textual printout of the tree"""
        result.append(f'{prefix}{self.function.__name__}{"("}\n')
        for i, child in enumerate(self.children):
            child.generate_tree_code(prefix + "   ", result)
            result.append(",")
            if i < len(self.children) - 1:
                result.append("\n")
        result.append(prefix + ")")

    @override
    def filter_nodes(
        self, filter_func: Callable, nodes: List[TreeNode]
    ) -> None:
        super().filter_nodes(filter_func, nodes)
        for child in self.children:
            child.filter_nodes(filter_func, nodes)

    @override
    def replace_child(self, old_child, new_child):
        for i, child in enumerate(self.children):
            if child is old_child:
                self.children[i] = new_child
                return
            child.replace_child(old_child, new_child)

    @override
    def __eq__(self, other):
        return (
            super().__eq__(other)
            and isinstance(other, FunctionNode)
            and self.function == other.function
            and self.children == other.children
        )

    @staticmethod
    def get_func_types(f: Callable) -> List[type]:
        """
        Return list of function types in the following format:
        [type_arg_1, type_arg_2, ..., type_arg_n, return_type]

        Parameters
        ----------
        f : Callable
            function (builtin or user-defined)

        Returns
        -------
        List[type]
            List of function types, sorted by argument order
            with the return type as the last element
        """
        params_types: Dict = get_type_hints(f)
        type_list = list(params_types.values())
        if not type_list:
            # If we don't have type hints, assign None types
            type_list = [NoneType] * (arity(f) + 1)
        return type_list

    def __repr__(self):
        return (
            f"{self.function.__name__}({', '.join(map(str, self.children))})"
        )


class TerminalNode(TreeNode):
    def __init__(self, value: Any, node_type=NoneType, parent=None) -> None:
        super().__init__(node_type, parent)
        self.value = value

    @override
    def depth(self):
        return 0

    @override
    def execute(self, **kwargs):
        """Recursively execute the tree by traversing it in a depth-first order"""

        if isinstance(self.value, Number):  # terminal is a constant
            return self.value
        # terminal is a variable, return its value if type matches
        kwarg_val = kwargs[self.value]

        # kwarg might be a numpy array
        kwarg_type = (
            type(kwarg_val.item(0))
            if isinstance(kwarg_val, np.ndarray)
            else type(kwarg_val)
        )

        if self.node_type is not NoneType and self.node_type != kwarg_type:
            raise TypeError(
                f"Expected {self.value} to be of type {self.node_type},"
                f"got {kwarg_type}."
            )
        return kwarg_val

    @override
    def generate_tree_code(self, prefix, result):
        """Recursively produce a simple textual printout of the tree"""
        result.append(f"{prefix}{str(self.value)}")

    @override
    def __eq__(self, other):
        return (
            super().__eq__(other)
            and isinstance(other, TerminalNode)
            and self.value == other.value
        )

    def __repr__(self):
        return str(self.value)
