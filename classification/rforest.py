# -*- coding: utf-8 -*-

from smile.classification import RandomForest as JRandomForest
from smile.classification import DecisionTree

from ..utils.smile_util import numeric_attributes

import mipylib.numeric as np
import math
from .classifer import Classifer

class RandomForest(Classifer):
    '''
    Random forest for classification. 

    Random forest is an ensemble classifier that consists of many decision trees and outputs the 
    majority vote of individual trees. The method combines bagging idea and the random selection 
    of features.

    :param x: (*array*) Training samples. 2D array.
    :param y: (*array*) Training labels in [0, c), where c is the number of classes.
    :param attributes: (*array*) Attribute properties.
    :param ntrees: (*int*) The number of trees.
    :param max_nodes: (*int*) The maximum number of leaf nodes in the tree.
    :param node_size: (*int*) Number of instances in a node below which the tree will not split.
    :param mtry: (*int*) the number of random selected features to be used to determine the 
        decision at a node of the tree. floor(sqrt(dim)) seems to give generally good performance, 
        where dim is the number of variables.
    :param sub_sample: (*float*) The sampling rate for training tree. 1.0 means sampling with 
        replacement. < 1.0 means sampling without replacement.
    :param split_rule: (*string*) The splitting rule. 
    :param class_weight: (*array*) Priors of the classes.
    '''
    
    def __init__(self, x=None, y=None, attributes=None, ntrees=500, max_nodes=-1, node_size=1,
            mtry=-1, sub_sample=1.0, split_rule='gini', class_weight=None):
        self._x = x
        self._y = y        
        self._attributes = attributes
        self._ntrees = ntrees        
        self._max_nodes = max_nodes
        self._node_size = node_size
        self._mtry = mtry
        self._sub_sample = sub_sample
        self._split_rule = split_rule    
        self._class_weight = class_weight
        if x is None or y is None:
            self._model = None
        else:
            self._learn()
        
    def _learn(self):
        p = self._x.shape[1]
        if self._attributes is None:
            self._attributes = numeric_attributes(p)
        m = int(math.floor(math.sqrt(p))) if self._mtry <= 0 else self._mtry
        j = self._x.shape[0] / self._node_size if self._max_nodes <= 1 else self._max_nodes
        split_rule = DecisionTree.SplitRule.valueOf(self._split_rule.upper())
        k = int(self._y.max()) + 1
        weight = np.ones(k, dtype='int') if self._class_weight is None  else self._class_weight
        self._model = JRandomForest(self._attributes, self._x.tojarray('double'),
            self._y.tojarray('int'), self._ntrees, j, self._node_size, m, 
            self._sub_sample, split_rule, weight.tojarray('int'))
    
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