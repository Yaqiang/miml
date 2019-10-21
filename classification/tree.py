# -*- coding: utf-8 -*-

from smile.classification import DecisionTree as JDecisionTree

from ..utils.smile_util import numeric_attributes

import mipylib.numeric as np
from .classifer import Classifer

class DecisionTree(Classifer):
    '''
    Decision tree for classification. 

    A decision tree can be learned by splitting the training set into subsets based on an attribute 
    value test. This process is repeated on each derived subset in a recursive manner called 
    recursive partitioning. The recursion is completed when the subset at a node all has the same 
    value of the target variable, or when splitting no longer adds value to the predictions.

    :param x: (*array*) Training samples. 2D array.
    :param y: (*array*) Training labels in [0, c), where c is the number of classes.
    :param max_nodes: (*int*) The maximum number of leaf nodes in the tree.
    :param attributes: (*array*) Attribute properties.
    :param split_rule: (*string*) The splitting rule. 
    '''
    
    def __init__(self, x=None, y=None, max_nodes=200, attributes=None, split_rule='gini'):
        self._x = x
        self._y = y
        self._max_nodes = max_nodes
        self._attributes = attributes
        self._split_rule = split_rule       
        if x is None or y is None:
            self._model = None
        else:
            self._learn()
        
    def _learn(self):
        if self._attributes is None:
            self._attributes = numeric_attributes(self._x.shape[1])
        self._model = JDecisionTree(self._attributes, self._x.tojarray('double'),
            self._y.tojarray('int'), self._max_nodes, 
            JDecisionTree.SplitRule.valueOf(self._split_rule.upper()))
    
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