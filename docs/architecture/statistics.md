# Statistics

The statistics class logs statistics on the population in each generation.

At the initialization of the Algorithm, Statistics register to a generation-end event, published by the Algorithm.

Statistics define an abstract `write_statistics` method.
The most common Statistics subclass is `BestAverageWorstStatistics`. This subclass logs the best, average and worst statistics for each generation.
