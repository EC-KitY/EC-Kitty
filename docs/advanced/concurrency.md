# Concurrency

Concurrency is maintained through builtin [Executor objects](https://docs.python.org/3/library/concurrent.futures.html).

Currently, only fitness computation is done concurrently, due to its high computational cost.

## Process Pool Executor
This executor computes fitness scores by creating multiple processes that can run on different CPUs in parallel. Note that this adds a slight overhead in runtime since process creation and inter-process communication is costly. Thus, this executor should be used for heavier fitness functions.

## Thread Pool Executor
This executor creates several threads for fitness computation. Due to Python's Global Interpreter Lock (GIL), only a single thread can be executed at a time.
This executor should be used if your fitness function releases the GIL frequently.
The GIL is released during I/O operations (e.g., opening a file or reading from a socket) and when invoking C functions, such as those used in `NumPy` ([NumPy vs GIL reference](https://superfastpython.com/numpy-vs-gil/)).

## Max Workers
The `max_workers` parameter determines the number of worker processes or threads to create. If set to `None`, it defaults to the maximum number supported by your hardware. However, using a high number of workers can result in frequent context switching, potentially causing significant overhead.

## Usage
Setting the desired Executor is done by passing the (optional) arguments `executor` and `max_workers` to the constructor of `SimpleEvolution`, as follows:
```python
algo = SimpleEvolution(
    # ...
    executor="process",  # or "thread"
    max_workers=3,
    # ...
)
```

## Additional concurrency usages
The executor is a field in Algorithm. Feel free to use it for parallel genetic operators, termination checking, or any other case you find suitable.
