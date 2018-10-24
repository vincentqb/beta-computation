def compute_return(col):
    """
    Compute relative difference.

    :param col: time series
    :return: time series of relative difference
    """
    col0 = col.shift(-1)
    return (col - col0)/col0
