from org.nd4j.linalg.learning.config import Nesterovs, Sgd, Adam, AdaGrad
from org.deeplearning4j.nn.weights import WeightInit
from org.deeplearning4j.nn.conf.distribution import UniformDistribution
from org.nd4j.linalg.lossfunctions import LossFunctions
from org.nd4j.linalg.lossfunctions.impl import LossMCXENT
from org.deeplearning4j.nn.api import OptimizationAlgorithm

def get_updater(updater):
    '''
    Get updater.
    :param updater: Updater dictionary.
    :return: Updater
    '''
    name = updater.pop('name', 'nesterovs').lower()
    if name == 'nesterovs':
        learn_rate= updater.pop('learn_rate', 0.01)
        momentum = updater.pop('momentum', 0.9)
        return Nesterovs(learn_rate, momentum)
    elif name == 'sgd':
        learn_rate = updater.pop('learn_rate', 0.1)
        return Sgd(learn_rate)
    elif name == 'adam':
        learn_rate = updater.pop('learn_rate', 1e-3)
        beta1 = updater.pop('beta1', 0.9)
        beta2 = updater.pop('beta2', 0.999)
        epsilon = updater.pop('epsilon', 1e-8)
        return Adam(learn_rate, beta1, beta2, epsilon)
    elif name == 'adagrad':
        learn_rate = updater.pop('learn_rate', 1e-1)
        epsilon = updater.pop('epsilon', 1e-6)
        return AdaGrad(learn_rate, epsilon)

def get_weight_init(kwargs):
    '''
    Get weight init
    :param kwargs: Weight init dictionary
    :return: Weight init
    '''
    name = kwargs.pop('name', 'xavier').lower()
    if name == 'xavier':
        return WeightInit.valueOf(name.upper())
    elif name == 'uniform':
        lower = kwargs.pop('lower', 0)
        upper = kwargs.pop('upper', 1)
        return UniformDistribution(lower, upper)

def get_loss_function(name, **kwargs):
    '''
    Get loss function
    :param name: (*string*) Loss function name
    :param kwargs: Loss function parameters
    :return: Loss function
    '''
    name = name.upper()
    if name == "LOSSMCXENT":
        weights = kwargs.pop('weights')
        return LossMCXENT(weights)
    else:
        return LossFunctions.LossFunction.valueOf(name)

def get_optimizer(name):
    """
    Get OptimizationAlgorithm enum
    :param name: (*string*) Optimizer name
    :return: OptimizationAlgorithm enum
    """
    name = name.upper()
    return OptimizationAlgorithm.valueOf(name)