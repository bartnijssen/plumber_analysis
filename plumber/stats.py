"""
Statistical functions for plumber
These are a superset of the functions used in [Best et al. 2015]
(http://dx.doi.org/10.1175/jhm-d-14-0158.1)
"""
import numpy as np
import pandas as pd


def calcAllStats(df1, df2):
    """Calculate all the stats and return dict"""
    stats = {}
    stats['Absolute bias'] = meanBiasError(df1, df2)
    stats['1 - stdev ratio'] = relativeStandardDeviation(df1, df2)
    stats['1 - Correlation'] = correlationMeasure(df1, df2)
    stats['Normalized mean absolute error'] = normalizedMeanError(df1, df2)
    stats['Difference in 5th percentile'] = absoluteDiffPercentile(df1,
                                                                   df2, 0.05)
    stats['Difference in 95th percentile'] = absoluteDiffPercentile(df1,
                                                                    df2, 0.95)
    stats['1 - skewness ratio'] = relativeSkewness(df1, df2)
    stats['1 - kurtosis ratio'] = relativeKurtosis(df1, df2)
    stats['1 - overlap statistic'] = 1 - histOverlap(df1, df2)
    return stats


def meanBiasError(df1, df2):
    """Mean bias error between dataframe d1 and d2"""
    return abs(df1.mean()-df2.mean())


def relativeStandardDeviation(df1, df2):
    """The difference between 1.0 and the ratio of the standard
       deviations of d1 and d2"""
    return abs(1 - df1.std()/df2.std())


def correlationMeasure(df1, df2):
    """Correlation coefficient between d1 and d2"""
    return 1 - df1.corrwith(df2)


def normalizedMeanError(df1, df2):
    """Normalized mean error between d1 and d2"""
    return abs(df1-df2).sum()/abs(df2.mean()-df2).sum()


def absoluteDiffPercentile(df1, df2, percentile=0.5):
    """Absolute difference in percentile between df1 and df2"""
    return abs(df1.quantile(percentile) - df2.quantile(percentile))


def relativeSkewness(df1, df2):
    """The difference between 1.0 and the ratio of the skewness
       of d1 and d2"""
    return abs(1 - df1.skew() / df2.skew())


def relativeKurtosis(df1, df2):
    """The difference between 1.0 and the ratio of the kurtosis
       of d1 and d2"""
    return abs(1 - df1.kurt() / df2.kurt())


def histOverlap(df1, df2, nbins=25):
    """Calculate the overlap statistic from [Perkins et al., 2007]
       (http://dx.doi.org/10.1175/Jcli4253.1)"""
    # Get the minimum values across the dataframes
    a1 = df1.min().dropna()
    a2 = df2.min().dropna()
    lower = pd.Series([min(a1[x], a2[x]) for x in sorted(a1.keys())
                       if x in a2.keys()],
                      [x for x in sorted(a1.keys()) if x in a2.keys()])
    a1 = df1.max().dropna()
    a2 = df2.max().dropna()
    upper = pd.Series([max(a1[x], a2[x]) for x in sorted(a1.keys())
                       if x in a2.keys()],
                      [x for x in sorted(a1.keys()) if x in a2.keys()])
    overlap = pd.Series(np.full(len(lower.keys()), np.nan),
                        sorted(lower.keys()))
    for var in sorted(lower.keys()):
        # to get nbins bins, you need one more boundary
        bins = np.linspace(lower[var], upper[var], nbins+1)
        hdf1 = np.histogram(df1[var], bins=bins)
        hdf2 = np.histogram(df2[var], bins=bins)
        overlap[var] = np.minimum(hdf1[0], hdf2[0]).sum()/len(df1[var])
    return overlap
