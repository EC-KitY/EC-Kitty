import random
import numpy as np


class RNG:
    """
    Random number generator.
    Necessary for experiment reproducibility.
    Currently supports `random` and `numpy` modules.
    For additional modules, extend this class and override `set_seed`.

    Example:
    class TorchRNG(RNG):
        @override
        def set_seed(self, seed: int) -> None:
            super().set_seed(seed)
            torch.manual_seed(seed)
    """

    def __init__(self) -> None:
        self._seed = None

    def set_seed(self, seed: int) -> None:
        """
        Set seed for random number generator.

        Parameters
        ----------
        seed : int
            Seed for random number generator
        """
        self._seed = seed
        random.seed(seed)
        np.random.seed(seed)
