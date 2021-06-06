from typing import List
import math 

def mean(xs: List[float]) -> float:
    """
    params:
        xs - list of numeric elements
    
    Mean calculation.
    """
    return sum(xs) / len(xs)

def de_mean(xs: List[float]) -> List[float]:
    """
    params:
        xs - list of numeric elements
    Translate xs by subtracting its mean (so the result has mean 0)
    """
    x_bar = mean(xs)
    return [x - x_bar for x in xs]

def dot(v: List[float], w: List[float]) -> float:
    """
    params:
        v - list of numeric elements
        w - list of numeric elements
    Computes v_1 * w_1 + ... + v_n * w_n
    """
    #vectors must be same length
    assert len(v) == len(w)

    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def sum_of_squares(v: List[float]) -> float:
    """
    params: 
        v - list of numeric elements
    Returns v_1 * v_1 + ... + v_n * v_n
    """
    return dot(v, v)

def variance(xs: List[float]) -> float:
    """
    params:
        xs - list of numeric elements
    
    Should be almost the average squared deviation from the mean
    """
    # Must have at least 2 elements
    assert len(xs) >= 2
    
    n = len(xs)
    deviations = de_mean(xs)
    return sum_of_squares(deviations) / (n-1)

def standard_deviation(xs: List[float]) -> float:
    """
    params:
        xs - list of numeric elements
    The standard deviation is the square root of the variance
    """
    return math.sqrt(variance(xs))

def annualize(x: float, p: int, m: int = 12) -> float:
    """
    Annualize a return by a the formula give:
    (1+R)^(m/p) -1, where
    R- Return
    m - year expressed in units of calculation steps
    p - calculation period expressed in units of calculation step
    """
    # to avoid division by zero
    assert p > 0
    return (1+x) ** (m/p) - 1


def subtract(v: List[float], w: List[float]) -> List[float]:
    """
    params:
        v - list of numeric elements
        w - list of numeric elements
    
    Subtract elements from one array to another, element wise.
    """
    # vectors must be the same length
    assert len(v) == len(w)

    return [v_i - w_i for v_i, w_i in zip(v, w)]


def dot(v: List[float], w: List[float]) -> float:
    """
    params:
        v - list of numeric elements
        w - list of numeric elements

    Computes v_1 * w_1 + ... + v_n * w_n
    """
    
    #vectors must be same length
    assert len(v) == len(w) 

    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def covariance(xs: List[float], ys: List[float]) -> float:
    """
    params:
        xs - list of numeric elements
        ys - list of numeric elements
    
    Measures the directional relationship.
    """
    
    #xs and ys must have same number of elements
    assert len(xs) == len(ys)

    return dot(de_mean(xs), de_mean(ys)) / (len(xs) - 1)


def correlation(xs: List[float], ys: List[float]) -> float:
    """
    params:
        xs - list of numeric elements
        ys - list of numeric elements
        
    Measures how much xs and ys vary in tandem about their means
    """
    stdev_x = standard_deviation(xs)
    stdev_y = standard_deviation(ys)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(xs, ys) / stdev_x / stdev_y
    else:
        # if no variation, correlation is zero
        return 0