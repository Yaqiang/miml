
from smile.clustering import DeterministicAnnealing as JDeterministicAnnealing

import mipylib.numeric as np
from .cluster import Cluster

class DeterministicAnnealing(Cluster):
    '''
    Deterministic annealing clustering.
    
    Deterministic annealing extends soft-clustering to an annealing process.
    For each temperature value, the algorithm iterates between the calculation
    of all posteriori probabilities and the update of the centroids vectors,
    until convergence is reached. The annealing starts with a high temperature.
    Here, all centroids vectors converge to the center of the pattern
    distribution (independent of their initial positions). Below a critical
    temperature the vectors start to split. Further decreasing the temperature
    leads to more splittings until all centroids vectors are separate. The
    annealing can therefore avoid (if it is sufficiently slow) the convergence
    to local minima.

    :param k_max: (*int*) The maximum number of clusters.
    :param alpha: (*float*) The temperature T is decreasing as T = T * alpha. alpha has to be 
        in (0, 1).
    '''
    
    def __init__(self, k_max, alpha=0.9):
        super(DeterministicAnnealing, self).__init__()
        
        self._k_max = k_max
        self._alpha = alpha        
        
    def fit(self, x):
        """
        Fitting data.
        
        :param x: (*array*) Input data.
        
        :returns: self.
        """
        self._model = JDeterministicAnnealing(x.tojarray('double'), self._k_max, self._alpha)
        return self
    
    def fit_predict(self, x):
        """
        Fitting and cluster data.

        :param x: (*array*) Input data.
        
        :returns: (*array*) The cluster labels.
        """
        self.fit(x)
        
        r = self._model.getClusterLabel()
        return np.array(r)
        
        
##############################################