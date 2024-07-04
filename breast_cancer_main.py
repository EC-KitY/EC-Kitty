"""
Solving a sklearn_mode problem created through scikit-learn's `load breast cancer`.
This is an sklearn setting so we use `fit` and `predict`.
"""

from time import time

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.base.typed_functions import (
    add2floats,
    div2floats,
    mul2floats,
    sub2floats,
)
from eckity.breeders.simple_breeder import SimpleBreeder
from examples.treegp.sklearn_mode.root_function_creator import (
    RootFunctionCreator,
)
from eckity.genetic_encodings.gp.tree.utils import create_terminal_set
from eckity.genetic_operators.crossovers.subtree_crossover import (
    SubtreeCrossover,
)
from eckity.genetic_operators.mutations.subtree_mutation import SubtreeMutation
from eckity.genetic_operators.selections.tournament_selection import (
    TournamentSelection,
)
from eckity.sklearn_compatible.classification_evaluator import (
    ClassificationEvaluator,
)
from eckity.sklearn_compatible.sk_classifier import SKClassifier
from eckity.statistics.best_avg_worst_size_tree_statistics import (
    BestAverageWorstSizeTreeStatistics,
)
from eckity.subpopulation import Subpopulation
from eckity.termination_checkers import ThresholdFromTargetTerminationChecker

# Adding your own types and functions

t_argmax = type("argmax", (int,), {})


def argmax2(x0: float, x1: float) -> t_argmax:
    return np.argmax([x0, x1])


def main():
    """
    Evolve a GP Tree that classifies breast cancer,
    using a dataset from sklearn
    """
    start_time = time()

    # load the brest cancer dataset from sklearn
    X, y = load_breast_cancer(return_X_y=True)

    # Automatically generate a terminal set.
    # Since there are 30 features, set terminal_set to: ['x0', 'x1', ..., 'x29']
    terminal_set = create_terminal_set(X)
    terminal_set = {x: float for x in terminal_set}

    # Define function set
    function_set = [argmax2, add2floats, sub2floats, mul2floats, div2floats]

    # Initialize SimpleEvolution instance
    algo = SimpleEvolution(
        Subpopulation(
            creators=RootFunctionCreator(
                root_function=argmax2,
                init_depth=(2, 4),
                terminal_set=terminal_set,
                function_set=function_set,
                bloat_weight=0.0001,
            ),
            population_size=100,
            evaluator=ClassificationEvaluator(metric=accuracy_score),
            # maximization problem (fitness is accuracy), so higher fitness is better
            higher_is_better=True,
            elitism_rate=0.05,
            # genetic operators sequence to be applied in each generation
            operators_sequence=[
                SubtreeCrossover(probability=0.9, arity=2),
                SubtreeMutation(probability=0.2, arity=1),
            ],
            selection_methods=[
                # (selection method, selection probability) tuple
                (
                    TournamentSelection(
                        tournament_size=4, higher_is_better=True
                    ),
                    1,
                )
            ],
        ),
        breeder=SimpleBreeder(),
        max_workers=1,
        max_generation=100,
        # optimal fitness is 1, evolution ("training") process will be finished when best fitness <= threshold
        termination_checker=ThresholdFromTargetTerminationChecker(
            optimal=1, threshold=0.03
        ),
        statistics=BestAverageWorstSizeTreeStatistics(),
    )
    # wrap the basic evolutionary algorithm with a sklearn-compatible classifier
    classifier = SKClassifier(algo)

    # split brest cancer dataset to train and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # fit the model (perform evolution process)
    classifier.fit(X_train, y_train)

    print("best individual:\n", algo.best_of_run_.root)

    # check training set results
    print(
        f"\nbest pure fitness over training set: {algo.best_of_run_.get_pure_fitness()}"
    )

    # check test set results by computing the accuracy score between the prediction result and the test set result
    test_score = accuracy_score(y_test, classifier.predict(X_test))
    print(f"test score: {test_score}")

    print(f"Total runtime: {time() - start_time} seconds.")


if __name__ == "__main__":
    main()
