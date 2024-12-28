"""
This module implements the SimpleEvolution class.
"""

from overrides import overrides

from eckity.algorithms.algorithm import Algorithm
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.evaluators import SimplePopulationEvaluator
from eckity.random import RNG
from eckity.termination_checkers import ThresholdFromTargetTerminationChecker


class SimpleEvolution(Algorithm):
    """
    Simple case evolutionary algorithm.

    Basic evolutionary algorithm that contains one subpopulation.
    Does not include and is not meant for multi-objective, co-evolution etc.
    Such algorithms should be implemented in a new Algorithm subclass.

    Parameters
    ----------
    population: Population
        The population to be evolved.
        Contains only one subpopulation in simple case.


    statistics: Union[Statistics, List[Statistics]], default=None
        Provide multiple statistics on the population during the evolution.

    breeder: SimpleBreeder
        Responsible for applying selection and operators on individuals
        in each generation. Applies on one subpopulation in simple case.

    population_evaluator: SimplePopulationEvaluator,
                          default=SimplePopulationEvaluator instance
            Responsible for evaluating each individual's fitness concurrently
            and returns the best individual of each subpopulation
            (returns a single individual in simple case).

    max_generation: int, default=1000
            Maximal number of generations to run the evolutionary process.
            Note the evolution could end before reaching max_generation,
            depending on the termination checker.

    events: dict(str, dict(object, function)), default=None
            Dictionary of events, where each event holds
            a dictionary of (subscriber, callback method).

    event_names: list of strings, default=None
            Names of events to publish during the evolution.

    termination_checker: TerminationChecker
            Checks if the evolution should perform early termination.

    max_workers: int, default=None
            Maximal number of worker nodes for the Executor object that
            evaluates the fitness of the individuals.

    random_generator: RNG
            Random number generator

    random_seed: int, default=current system time
            Initial random seed for deterministic experiment.

    generation_seed: int, default=None
            Current generation seed.
            Useful for resuming a previously paused experiment.

    best_of_run_: Individual, default=None
            The individual with the best fitness in the entire evolution.

    best_of_gen: Individual, default=None
            The individual that has the best fitness in the current generation.

    worst_of_gen: Individual, default=None
            The individual that has the worst fitness in current generation.

    generation_num: int, default=0
            Current generation number
    """

    def __init__(
        self,
        population,
        statistics=None,
        breeder: SimpleBreeder = SimpleBreeder(),
        population_evaluator: SimplePopulationEvaluator = None,
        max_generation=500,
        events=None,
        event_names=None,
        termination_checker=None,
        executor="thread",
        max_workers=None,
        random_generator: RNG = RNG(),
        random_seed=None,
        generation_seed=None,
        best_of_run_=None,
        best_of_gen=None,
        worst_of_gen=None,
        generation_num=0,
    ):

        if event_names is None:
            _event_names = [
                "before_eval",
                "after_eval",
                "before_breeding",
                "after_breeding",
            ]
        else:
            _event_names = event_names

        if statistics is None:
            statistics = []

        if breeder is None:
            breeder = SimpleBreeder()
        
        if population_evaluator is None:
            population_evaluator = SimplePopulationEvaluator()

        if not isinstance(breeder, SimpleBreeder):
            raise ValueError(
                f"Expected SimpleBreeder, got {type(breeder)}."
            )
        
        if not isinstance(population_evaluator, SimplePopulationEvaluator):
            raise ValueError(
                "Expected SimplePopulationEvaluator, "
                f"got {type(population_evaluator)}."
            )

        super().__init__(
            population,
            statistics=statistics,
            breeder=breeder,
            population_evaluator=population_evaluator,
            events=events,
            event_names=_event_names,
            executor=executor,
            max_workers=max_workers,
            random_generator=random_generator,
            random_seed=random_seed,
            generation_seed=generation_seed,
            termination_checker=termination_checker,
            generation_num=generation_num,
        )

        self.termination_checker = termination_checker
        self.best_of_run_ = best_of_run_
        self.best_of_gen = best_of_gen
        self.worst_of_gen = worst_of_gen
        self.max_generation = max_generation

        self.final_generation_ = None

    def initialize(self):
        """
        Initialize the evolutionary algorithm

        Register statistics to `after_generation` event
        """
        super().initialize()
        for stat in self.statistics:
            self.register("after_generation", stat.write_statistics)

    @overrides
    def generation_iteration(self, gen: int) -> bool:
        """
        Performs one iteration of the evolutionary run,
        for the current generation

        Parameters
        ----------
        gen:
                current generation number (for example, generation #100)

        Returns
        -------
        None.
        """

        # breed population
        self.breeder.breed(self.population)

        # Evaluate the entire population and get the best individual
        self.best_of_gen = self.population_evaluator.act(self.population)

        if self.best_of_gen.better_than(self.best_of_run_):
            self.best_of_run_ = self.best_of_gen

        self.worst_of_gen = self.population.sub_populations[
            0
        ].get_worst_individual()

    def execute(self, **kwargs):
        """
        Compute output using best evolved individual.
        Use `execute` in a non-sklearn setting.
        Input keyword arguments that set variable values.
        For example if `terminal_set=['x', 'y', 1, -1]`
        then call `execute(x=..., y=...)`.

        Parameters
        ----------
        **kwargs : keyword arguments
                The input to the program (tree).

        Returns
        -------
        object
                Output as computed by the best individual of the evolution.

        """
        return self.best_of_run_.execute(**kwargs)

    def finish(self):
        """
        Finish the evolutionary run by showing the best individual
        and printing the best fitness
        """
        super().finish()
        self.best_of_run_.show()

    def get_individual_evaluator(self):
        return self.population.sub_populations[0].evaluator

    def get_average_fitness(
        self,
    ):  # TODO move this function to statistics
        return self.population.get_average_fitness()

    def event_name_to_data(self, event_name):
        if event_name == "init":
            return {
                "population": self.population,
                "statistics": self.statistics,
                "breeder": self.breeder,
                "termination_checker": self.termination_checker,
                "max_generation": self.max_generation,
                "events": self.events,
                "max_workers": self.max_workers,
                "generation_num": self.generation_num,
            }

        # default case
        return {
            "population": self.population,
            "best_of_run_": self.best_of_run_,
            "best_of_gen": self.best_of_gen,
            "generation_num": self.generation_num,
        }
