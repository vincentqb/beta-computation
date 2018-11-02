import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def compute_return(df, groups):
    """
    Compute relative difference.

    :param df: data frame
    :param groups: groups
    :return: time series of relative difference
    """

    df0 = df.sort_index().groupby(groups).shift(1)
    df1 = df.sort_index().groupby(groups).shift(0)
    s = (df1 - df0)/df0
    s.name = "return"
    return s


def attach_return(df, *args, **kwargs):
    """
    Attach relative difference column.

    :param df: data frame
    :return: data frame representation of time series of relative difference
    """

    s = compute_return(df, *args, **kwargs)
    return df.to_frame().join(s.to_frame())


class LS:

    def __init__(self, kind="sklearn"):
        self.numpy = numpy

    def fit(self, X, Y):
        if self.numpy:
            A = np.vstack([X.values, np.ones(len(X.values))]).T
            m, c = np.linalg.lstsq(A, Y, rcond=None)[0]
            self.coef = m
            self.const = c
        else:
            lr = LinearRegression(n_jobs=-1)
            lr.fit(
                X.values.reshape(-1,1),
                Y.values.reshape(-1,1)
            )
            self.coef = lr.coef_[0][0]
            self.const = lr.intercept_
        return self


def rolling_regression(df, col_X, col_Y, group_col=None, window=1, numpy=False):
    """
    Compute rolling betas.

    :param df: data frame
    :param col_X: name of column for X variable
    :param col_Y: name of column for Y variable
    :param group_col: name of column for grouping
    :param window: lenght of window
    :return: series of betas
    """

    # TODO Optimize using numpy to avoid looping over groups and windows

    ls = LS(numpy=numpy)

    def reg(d, group=None):
        ls.fit(d[col_X], d[col_Y])
        coef = ls.coef
        if group:
            return ((group, d.index[-1]), coef)
        else:
            return (d.index[-1], coef)

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


def attach_beta(df, *args, **kwargs):
    """
    Attach rolling beta column.

    :param df: data frame
    :param col_X: name of column for X variable
    :param col_Y: name of column for Y variable
    :param group_col: name of column for grouping
    :param window: lenght of window
    :return: series of betas
    """

    o = rolling_regression(df, *args, **kwargs)
    return df.join(o.to_frame())
