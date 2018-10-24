def compute_return(df, groups):
    """
    Compute relative difference.

    :param col: time series
    :return: time series of relative difference
    """
    df0 = df.sort_index().groupby(groups).shift(1)
    df1 = df.sort_index().groupby(groups).shift(0)
    return (df1 - df0)/df0
