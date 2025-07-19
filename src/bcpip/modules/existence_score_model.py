import numpy as np


def existence_score_model(x: np.ndarray) -> np.ndarray:
    """Scoring model used in converting features (eg. identity) to scores.

    Args:
        x: Features to be converted to scores

    Returns:
        An array of converted scores
    """
    # prob. ver.1
    # x = x[x >= 40]
    # y = 0.18 * np.log(0.15 * (x - 40) + 1) + 0.6
    # y = np.minimum(y, 1)

    # prob. ver.2
    y = 1 / (1 + np.exp(-1 / 10 * (x - 40)))

    # prob. ver.3
    # y = 1/100 * x
    return y
