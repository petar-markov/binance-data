from typing import List
import math
from math_helpers import subtract, mean, standard_deviation, annualize

def sharpe_ratio(xs: List[float], p: int = 0, RFR: List[float] = []) -> float:
    """ Compute the Sharpe Ratio"""
    
    # By default this will be with no RFR, due to numerous reasons
    # Most fundamental one is that this is pretty subjective for cryptos
    
    if not RFR:
        RFR = [0 for x in xs]

    assert len(xs) == len(RFR)
    
    # excess return
    r = subtract(xs, RFR)
    rm = mean(r)
    s = standard_deviation(xs)
    # We annualize only if priod is > 1 Year
    if p > 12:
        rm = annualize(rm, p)
        s = s * math.sqrt(12)
    
    return rm/s

def sortino_ratio(xs: List[float], p: int = 0, MAR: float = 0.0) -> float:
    """ 
    Compute Sortino Ratio 
    
    In this version we use minimum acceptance return (MAR),
    where in the mean calculation, we target only returns < MAR.
    Again this is by default 0.
    This helps to measure of the true risk incurred, i.e. the risk of achieving a
    return below the expected return.
    
    """
    
    #excess return
    r = [x for x in xs if x < MAR]
    if not r:
        return 0
    rm = mean(r) - MAR
    s = standard_deviation(r)
    # We annualize only if priod is > 1 Year
    if p > 12:
        rm = annualize(rm, p)
        s = s * math.sqrt(12)
    
    return rm / s