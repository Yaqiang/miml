# -*- coding: utf-8 -*-

from smile.regression import GradientTreeBoost as JGradientTreeBoost

from ..utils.smile_util import numeric_attributes

import mipylib.numeric as np
import math
from .regressor import Regressor

class GradientTreeBoost(Regressor):
    '''
    Gradient boosting for regression. 

    Gradient boosting is typically used with decision trees (especially CART regression trees) of 
    a fixed size as base learners. For this special case Friedman proposes a modification to 
    gradient boosting method which improves the quality of fit of each base learner.

    :param x: (*array*) Training samples. 2D array.
    :param y: (*array*) Training labels in [0, c), where c is the number of classes.
    :param attributes: (*array*) Attribute properties.
    :param loss: (*string*) Loss function for regression. By default, least absolute deviation is 
        employed for robust regression.
    :param ntrees: (*int*) The number of trees.
    :param max_nodes: (*int*) The maximum number of leaf nodes in the tree.
    :param shrinkage: (*float*) The shrinkage parameter in (0, 1] controls the learning rate of 
        procedure.
    :param sub_sample: (*float*) The sampling rate for training tree. 1.0 means sampling with 
        replacement. < 1.0 means sampling without replacement.
    '''
    
    def __init__(self, x=None, y=None, attributes=None, loss='LeastAbsoluteDeviation', ntrees=500, 
            max_nodes=6, shrinkage=0.05, sub_sample=0.7):
        self._x = x
        self._y = y        
        self._attributes = attributes
        self._loss = loss
        self._ntrees = ntrees        
        self._max_nodes = max_nodes
        self._shrinkage = shrinkage
        self._sub_sample = sub_sample
        if x is None or y is None:
            self._model = None
        else:
            self._learn()
        
    def _learn(self):
        p = self._x.shape[1]
        if self._attributes is None:
            self._attributes = numeric_attributes(p)
        loss = JGradientTreeBoost.Loss.valueOf(self._loss)
        self._model = JGradientTreeBoost(self._attributes, self._x.tojarray('double'),
            self._y.tojarray('double'), loss, self._ntrees, self._max_nodes, self._shrinkage, 
            self._sub_sample)
    
    def learn(self, x=None, y=None):
        """
        Learn from input data and labels.
        
        :param x: (*array*) Training samples. 2D array.
        :param y: (*array*) Training labels in [0, c), where c is the number of classes.
        """ 
        if not x is None:
            self._x = x
        if not y is None:
            self._y = y
        self._learn()
        
        
##################################################