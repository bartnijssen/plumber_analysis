"""
Plotting functions for plumber
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from . import io
from . import fargs
from . utils import flatten
callme = fargs.callFuncBasedOnDict


def getFigSize(info):
    """Create figsize from figwidth and figheight or return default"""
    try:
        return (info['figwidth'], info['figheight'])
    except KeyError:
        return mpl.rcParams['figure.figsize']


def getLimits(info, values):
    """Get the range of values"""
    try:
        low = info['lower']
    except KeyError:
        low = np.nanmin(values)
    try:
        high = info['upper']
    except KeyError:
        high = np.nanmax(values)
    try:
        if info['symmetric']:
            limit = np.abs([np.nanmax(values), np.nanmin(values)]).max()
            low = -limit
            high = limit
    except KeyError:
            pass
    return (low, high)


def plotHovmollerDoyHod(df, zlimits, cmap, ax):
    """Hovmoller plot of day of year versus hour of day"""
    grouped = df.groupby([lambda x: x.dayofyear,
                          lambda x: x.hour + x.minute/60]).mean().unstack()
    x = np.asarray(grouped.axes[1])
    y = np.asarray(grouped.axes[0])
    im = ax.axes.pcolormesh(x, y, grouped.values, vmin=zlimits[0],
                            vmax=zlimits[1], cmap=cmap)
    ax.axes.axis([x.min(), x.max(), y.min(), y.max()])
    return im


def setLegend(axes):
    """Make the legend visible in selected panels only (top left panel)"""
    for ax in flatten(axes):
        ax.legend().set_visible(False)
    ax = axes[0][0].legend().set_visible(True)


def setPlotDefaults(plotdict):
    """Set plot defaults based on plotdict"""
    if plotdict is None or not plotdict:
        return
    for key, val in plotdict.items():
        # mpl.rcParams.update({key: val})
        try:
            mpl.rcParams[key] = val
        except KeyError:
            pass


def setXYLabels(axes, info, **kwargs):
    """Set the x- and y-axis labels"""
    for i in range(axes.shape[0]):
        callme(axes[i][0].set_ylabel, info, **kwargs)
    for i in range(axes.shape[1]):
        callme(axes[-1][i].set_xlabel, info, **kwargs)


def setupPlotGrid(nrows, ncols, sharex='all', sharey='all', squeeze=None,
                  subplot_kw=None, *args, **kwargs):
    """Setup the plotting grid for a plot with nrows x ncols panels"""
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharex=sharex,
                           sharey=sharey, squeeze=squeeze,
                           subplot_kw=subplot_kw, *args, **kwargs)
    return (fig, ax)


class Plot(object):
    """Base class for plotting. This just sets up the overall plot. Each plot
       consists of one or more panels, """

    def __init__(self, plotdict):
        """Initialize Plot instance based on a dictionary with plot info."""
        if plotdict is None or plotdict is not type(dict):
            raise ValueError
        else:
            self.plotdict = plotdict
        self.fig, self.ax = plt.subplots(**self.plotdict['figure'])

    @classmethod
    def fromConfigFile(cls, configfile, section):
        """Initialize Plot Instance based on a configuration file. The section
           indicates the section in the configuration file to read"""
        cfg = io.parseConfig(configfile)
        return cls(cfg[section])


def plot_mean_diurnal_by_site_single_var(p, section, **kwargs):
    """Plot the mean diurnal cycle by site for selected models

    Parameters
    ----------
    Required:
        p : PlumberAnalysis instance
        section : key for p.cfg that has info that is specific to this plot,
                  i.e. p.cfg[section]

    Returns
    -------
    fig : matplotlib Figure instance
    """

    setPlotDefaults(p.cfg['plot_defaults'])
    info = p.cfg[section]
    info['figsize'] = getFigSize(info)

    fig, axes = callme(plt.subplots, info, squeeze=False,
                       figsize=info['figsize'], **kwargs)

    sites = sorted(p.data)
    for site, ax in zip(sites, flatten(axes)):
        for source in sorted(p.data[site]):
            df = p.data[site][source]
            try:
                df[info['read_vars']].\
                    groupby(lambda x: x.hour +
                            x.minute/60).mean().plot(ax=ax, label=source)
            except KeyError:
                pass

    for site, ax in zip(sites, flatten(axes)):
        ax.text(0.05, 0.95, site, horizontalalignment='left',
                verticalalignment='top', transform=ax.transAxes)
    axes[0][0].text(0.05, 0.85, info['read_vars'], horizontalalignment='left',
                    verticalalignment='top', transform=axes[0][0].transAxes)

    setXYLabels(axes, info, **kwargs)
    setLegend(axes)
    fig.tight_layout()

    callme(fig.savefig, info, filename=info['plotfilename'], **kwargs)


def plot_hovmuller_doy_vs_hod_by_year(p, section, **kwargs):
    """Plot a hovmuller plot by year with hour of day on the horizontal axis
       and day of year on the vertical axis

    Parameters
    ----------
    Required:
        p : PlumberAnalysis instance
        section : key for p.cfg that has info that is specific to this plot,
                  i.e. p.cfg[section]

    Returns
    -------
    fig : matplotlib Figure instance
    """

    setPlotDefaults(p.cfg['plot_defaults'])
    info = p.cfg[section]
    info['figsize'] = getFigSize(info)

    site = info['site']
    source = info['source']
    var = info['read_vars']

    d = p.data[site][source][var]
    years = []
    for year in range(d.index[0].year, d.index[-1].year+1):
        if d[str(year)].shape[0] > 100:
            years.append(year)

    nrows = 1
    ncols = len(years)

    fig, axes = callme(plt.subplots, info, nrows=nrows, ncols=ncols,
                       squeeze=False, figsize=info['figsize'], **kwargs)
    cmap = plt.get_cmap(info['cmap'])
    zlimits = getLimits(info, d.values)

    for ax, year in zip(axes.flat, years):
        df = d[str(year)]
        im = plotHovmollerDoyHod(df, zlimits, cmap, ax)

    if 'label' not in info:
        info['label'] = var

    callme(fig.colorbar, info, mappable=im, ax=axes.ravel().tolist(),
           label=info['label'])

    info['ylabel'] = 'Day of year'
    info['xlabel'] = 'Hour of day'

    for ax, year in zip(axes.flat, years):
        ax.text(0.05, 0.95, year, horizontalalignment='left',
                verticalalignment='top', transform=ax.transAxes)
    axes[0][0].text(0.05, 0.85, var, horizontalalignment='left',
                    verticalalignment='top', transform=axes[0][0].transAxes)
    axes[0][0].text(0.05, 0.75, '{} @ {}'.format(source, site),
                    horizontalalignment='left', verticalalignment='top',
                    transform=axes[0][0].transAxes)

    setXYLabels(axes, info, **kwargs)

    callme(fig.savefig, info, filename=info['plotfilename'], **kwargs)


def plot_hovmuller_doy_vs_hod_by_year_comparison(p, section, **kwargs):
    """Plot a hovmuller plot by year with hour of day on the horizontal axis
       and day of year on the vertical axis. Top row will be source 1, seconds
       row will be source 2, and the third row will be source 1-2

    Parameters
    ----------
    Required:
        p : PlumberAnalysis instance
        section : key for p.cfg that has info that is specific to this plot,
                  i.e. p.cfg[section]

    Returns
    -------
    fig : matplotlib Figure instance
    """

    setPlotDefaults(p.cfg['plot_defaults'])
    info = p.cfg[section]
    info['figsize'] = getFigSize(info)

    site = info['site']
    source1, source2 = info['source'][0:2]
    var = info['read_vars']

    d1 = p.data[site][source1][var]
    d2 = p.data[site][source2][var]
    years = []
    for year in range(d1.index[0].year, d1.index[-1].year+1):
        if d1[str(year)].shape[0] > 100:
            years.append(year)

    nrows = 3
    ncols = len(years)

    fig, axes = callme(plt.subplots, info, nrows=nrows, ncols=ncols,
                       squeeze=False, figsize=info['figsize'], **kwargs)

    cmap = plt.get_cmap(info['cmap'])
    zlimits = getLimits(info, d1.values+d2.values)
    for row, d in enumerate([d1, d2]):
        for ax, year in zip(axes[row, :].flat, years):
            df = d[str(year)]
            im = plotHovmollerDoyHod(df, zlimits, cmap, ax)

    callme(fig.colorbar, info, mappable=im, ax=axes[0:2, :].ravel().tolist(),
           label=info['label'])

    d = d1 - d2
    cmap = plt.get_cmap(info['cmap_diff'])
    zlimits = getLimits(info, d.values)
    for ax, year in zip(axes[2, :].flat, years):
        df = d[str(year)]
        im = plotHovmollerDoyHod(df, zlimits, cmap, ax)

    callme(fig.colorbar, info, mappable=im, ax=axes[2, :].ravel().tolist(),
           label='Delta {}'.format(info['label']))

    info['ylabel'] = 'Day of year'
    info['xlabel'] = 'Hour of day'

    for ax, year in zip(axes[0, :].flat, years):
        ax.text(0.05, 0.95, year, horizontalalignment='left',
                verticalalignment='top', transform=ax.transAxes)
    axes[0][0].text(0.05, 0.85, var, horizontalalignment='left',
                    verticalalignment='top', transform=axes[0][0].transAxes)
    axes[0][0].text(0.05, 0.75, '{} @ {}'.format(source1, site),
                    horizontalalignment='left', verticalalignment='top',
                    transform=axes[0][0].transAxes)
    axes[1][0].text(0.05, 0.75, '{} @ {}'.format(source2, site),
                    horizontalalignment='left', verticalalignment='top',
                    transform=axes[1][0].transAxes)
    axes[2][0].text(0.05, 0.75, '{} - {}'.format(source1, source2),
                    horizontalalignment='left', verticalalignment='top',
                    transform=axes[2][0].transAxes)

    setXYLabels(axes, info, **kwargs)

    callme(fig.savefig, info, filename=info['plotfilename'], **kwargs)
