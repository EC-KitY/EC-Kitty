# Randomness and reproducibility
By their nature, Evolutionary Algorithms contain randomness.
At the start of an experiment, a random seed is defined.
Then, at the start of each generation, another random seed, called "generation seed", is set.
This enables reproducing the experiment from scratch, or from a certain generation.

This is done by the RNG (Random Number Generation) object, which is a field in Algorithm.

RNG currently supports the `random` and `numpy` packages.

Supported methods such as `random.choice`, `numpy.random.randint` can be used as usual, without having to manually handle seeds.

Support for additional packages that generate random numbers can be done by extending this class and overriding the set_seed method, for instance:

```python
class TorchRNG(RNG):
    @override
    def set_seed(self, seed: int) -> None:
        super().set_seed(seed)
        torch.manual_seed(seed)

algo = SimpleEvolution(
    # some args
    random_generator=TorchRNG()
)
```
