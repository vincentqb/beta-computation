import pandas as pd
from sklearn.linear_model import LinearRegression


def compute_return(df, groups):
    """
    Compute relative difference.

    :param col: time series
    :return: time series of relative difference
    """

    df0 = df.sort_index().groupby(groups).shift(1)
    df1 = df.sort_index().groupby(groups).shift(0)
    s = (df1 - df0)/df0
    s.name = "return"
    return s

def attach_return(df, groups):
    """
    Attach relative difference column.

    :param col: time series
    :return: time series of relative difference
    """

    s = compute_return(df, groups)
    return df.to_frame().join(s.to_frame())


def rolling_regression(df, col_X, col_Y, group_col=None, window=1):
    """
    Compute rolling betas.

    :param df: data frame
    :param col_X: name of column for X variable
    :param col_Y: name of column for Y variable
    :param group_col: name of column for grouping
    :param window: lenght of window
    :return: series of betas
    """

    model_ols = LinearRegression()

    def reg(d, group=None):
        model_ols.fit(
            d[col_X].values.reshape(-1,1),
            d[col_Y].values.reshape(-1,1)
        )
        if group:
            return ((group, d.index[-1]), model_ols.coef_[0][0])
        else:
            return (d.index[-1], model_ols.coef_[0][0])

    if group_col:
        df = df.reset_index(group_col)
        l = []
        for name, group in df.groupby(group_col):
            curr = pd.Series(dict([
                        reg(group.iloc[(max(0,i-window+1)):(i+1)], name) for i in range(len(group))
                    ]))
            l.append(curr)
        output = pd.concat(l)
        output.name = "beta"
        output.index.names = [group_col] + df.index.names
        return output
    else:
        output = pd.Series(dict([
                    reg(df.iloc[(max(0,i-window+1)):(i+1)]) for i in range(len(df))
                ]))
        output.name = "beta"
        output.index.names = [group_col] + df.index.names
        return output.set_names(df.index.names)


def attach_beta(df, col_X, col_Y, group_col=None, window=1):
    """
    Attach rolling beta column.

    :param df: data frame
    :param col_X: name of column for X variable
    :param col_Y: name of column for Y variable
    :param group_col: name of column for grouping
    :param window: lenght of window
    :return: series of betas
    """

    o = rolling_regression(df, col_X, col_Y, group_col, window)
    return df.join(o.to_frame())
