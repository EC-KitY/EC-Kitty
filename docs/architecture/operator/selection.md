# Selection

Selection is done during the breeding process.

The abstract class `SelectionMethod` defines an abstract `select` function.
`select` select from 

Note that selection methods should create **new copies** of the selected individuals, using the method `individual.clone()`.
