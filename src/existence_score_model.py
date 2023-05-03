"""
==================================================================
Scoring model used in converting features (eg. identity) to scores 
==================================================================

Parameters
----------
x : numpy.array
    Features to be converted to scores

Return
------
y : numpy.array
    Scores

"""

import numpy as np

def existence_score_model(x, param):
    # prob. ver.1
    # x = x[x >= 40]
    # y = 0.18 * np.log(0.15 * (x - 40) + 1) + 0.6
    # y = np.minimum(y, 1)

    # prob. ver.2
    y = 1/(1+np.exp(-1/param * (x - 40)))
    
    # prob. ver.3
    # y = 1/100 * x
    return y