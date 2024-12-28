# Creator

The Creator is responsible for the creating the first generation of the evolutionary experiment.

Creator defines an abstract method `create_individuals` that must be implemented in its subclasses.

## GA Creators

There are several creators for initializing GA individuals - BitStringVectorCreator, IntVectorCreator and FloatVectorCreator.

## GP Creators

Currently only tree representation is supported in GP.
Trees can be initialized in grow, full or ramped-half-and-half methods, each having a creator of its own.
