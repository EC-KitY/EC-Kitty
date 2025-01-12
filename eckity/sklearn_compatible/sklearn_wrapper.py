from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_is_fitted, check_X_y


class SklearnWrapper(BaseEstimator):
    """
    Sklearn-compatible wrapper to support evolution using sklearn methods.

    Parameters
    ----------
    algorithm: Algorithm
        Wrapped Evolutionary algorithm.
        The Wrapper invokes 'evolve' and 'execute' methods of the algorithm
        during the fitting and prediction process, respectively.

    Attributes
    ----------
    is_fitted: bool
        Determines if the model is fitted (evolved).
    """

    def __init__(self,
                 algorithm):
        self.algorithm = algorithm

    def fit(self, X, y=None):
        """
       Run evolutionary algorithm.
       Use `fit` in a sklearn setting.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,) or (n_samples, n_outputs)
            The target values (real numbers).
        Returns
        -------
        self : SklearnWrapper
            Fitted (evolved) model.
        """
        # Check that X and y have correct shape
        X, y = check_X_y(X, y)

        for sub_pop in self.algorithm.population.sub_populations:
            sub_pop.evaluator.set_context((X, y))

        self.algorithm.evolve()
        self.is_fitted_ = True
        return self

    def predict(self, X):
        """
        Compute output using best evolved individual.
        Use `predict` in a sklearn setting.
        Input is a numpy array.

        Parameters
        ----------
        X : array-like or sparse matrix of (num samples, num feautres)

        Returns
        -------
        y : array, shape (num samples,)
            Returns predicted values.

        """

        # Check is fit had been called
        check_is_fitted(self)

        return self.algorithm.best_of_run_.execute(X)

    # def __sklearn_is_fitted__(self):
    #     return self.is_fitted_

    def get_params(self, deep=True):
        return self.__getstate__()

    def set_params(self, **parameters):
        self.algorithm.__setstate__(parameters)
        return self

    def partial_fit(self, X, y, classes=None):
        raise NotImplementedError('not implemented yet')
        pass

    def __getstate__(self):
        state = self.__dict__.copy()
        if 'is_fitted_' in state:
            del state['is_fitted_']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
