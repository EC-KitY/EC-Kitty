# Operators
Each major class in EC-KitY extends the Operator class. Subclasses of Operator publish events before and after applying the operator,allowing other objects to register an event hook to these events.

For instance, Evaluator publishes an event before and after evaluating the fitness scores, selection methods publish events before and after the selection process, etc.
