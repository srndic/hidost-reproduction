# -*- coding: utf-8 -*-

import math
import operator

from matplotlib.colors import LogNorm
from matplotlib.figure import figaspect
import numpy
import pylab

# A color palette with 4 colors
colors4 = {'normal': ['#E8392B',   # red
                      '#E8852B',   # orange
                      '#21B13A',   # green
                      '#1C808E'],  # blue
           'lighter': ['#F8685D',
                       '#F8A75D',
                       '#47BE5C',
                       '#3A8C98'],
           'lightest': ['#FFA199',
                        '#FFCA99',
                        '#80D58F',
                        '#71B1BA'],
           'darker': ['#C0170A',
                      '#C0610A',
                      '#079320',
                      '#086875'],
           'darkest': ['#970B00',
                       '#974900',
                       '#007414',
                       '#01515D']
           }


def init_eurasip_style(left_margin=0.10,
                   right_margin=0.02,
                   top_margin=0.08,
                   bottom_margin=0.12,
                   figure_width=422.52348,
                   figure_height=None,
                   horizontal=True):
    pylab.close("all")
    fig_width_pt = figure_width
    inches_per_pt = 1.0 / 72.27                    # Convert pt to inch
    figure_width = fig_width_pt * inches_per_pt    # width in inches
    golden_mean = (math.sqrt(5) - 1.0) / 2.0         # Aesthetic ratio
    if figure_height is None:
        if horizontal:
            figure_height = figure_width * golden_mean
        else:
            figure_height = figure_width / golden_mean
    else:
        figure_height = figure_height * inches_per_pt
    fig_size = [figure_width, figure_height]
    params = {
        'backend': 'ps',
        'patch.linewidth': 0.6,
        'axes.linewidth': 0.6,
        'lines.markeredgewidth': 0.4,
        'lines.markersize': 2,
        'axes.labelsize': 7,
        'axes.titlesize': 7,
        'text.fontsize': 7,
        'legend.fontsize': 7,
        'xtick.labelsize': 7,
        'ytick.labelsize': 7,
        'text.usetex': True,
        'text.latex.preamble': [
            r'\usepackage[cm]{sfmath}'
        ],  # forces use of sans-serif CM font in math mode
        'figure.subplot.left': left_margin,
        'figure.subplot.right': 1 - right_margin,
        'figure.subplot.bottom': bottom_margin,
        'figure.subplot.top': 1 - top_margin,
        'figure.subplot.wspace': 0.15,
        'figure.subplot.hspace': 0.15,
        'figure.dpi': 600,
        'font.family': 'sans-serif',
        'font.serif': 'cm',
        'font.sans-serif': 'cm',
        'figure.figsize': fig_size,
        'lines.antialiased': True,
        'lines.linewidth': 0.6}
    import matplotlib
    matplotlib.rcParams.update(params)


def sorted_multicomparison(datas,
                           methods,
                           legend,
                           ylabels,
                           xlabel,
                           xticklabels,
                           plotfs,
                           autofmt_xdate=False,
                           subtitles=None):
    '''
Plots a sorted comparison of multiple methods' results across
multiple metrics.

For every metric a subplot is produced comparing the results
of all methods. The x axis is shared among all subplots. The
results are plotted using plot() and scatter() to emphasize
individual points.

  datas - an [n x 1] list of [m x 1] list of [1 x p] lists,
          where n is the number of metrics, m is the number
          of methods and p is the number of data points in
          every result
  methods - a [m x 1] list of method names (strings)
  legend - argument of the matplotlib legend() method
           (string) with an optional suffix '/N', where
           0 <= N < n determines which subplot to place
           the legend in
  ylabels - a [n x 1] list of metric names (strings) that will
            be used as y axis labels
  xlabel - x axis label
  xticklabels - labels for x axis ticks
  plotfs - a list of file names in which the plots should be
           saved
  autofmt_xdate - True if x tick labels are overlapping and
                  should be pretty-formatted
  subtitles - a list of titles, one for every subplot, or
              None for no subtitles
    '''
    c = colors4['normal']  # colors
    mfc = colors4['darkest']  # marker face colors
    mec = colors4['darkest']  # marker edge colors
    m = ['o', 'v', 's', '^']  # marker styles

    fig, axes = pylab.subplots(len(datas), 1, sharex=True)
    if len(datas) == 1:
        axes = [axes]
    for li, (data, ax) in enumerate(zip(datas, axes)):
        # Sort data vectors by sum of their Manhattan distance
        mv = [(method, vector) for method, vector in zip(methods, data)]
        mv.sort(key=lambda d: sum(d[1]))

        # Plot lines
        x_data = range(len(data[0]))
        for i, (method, y_data) in enumerate(mv):
            mi = methods.index(method)  # color by method order
            ax.plot(x_data, y_data, label=method, color=c[mi], marker=m[mi],
                    markerfacecolor='w', markeredgecolor=mec[mi],
                    markersize=2.7, markeredgewidth=1, linewidth=1.25,
                    zorder=2 * i / 100.0 + 1)
#            ax.scatter(x_data, y_data, s=8, color=dc[mi],
#                       zorder=2 * i / 100.0 + 1.01,
#                       linewidths=1, facecolors='w')

        # Set up y axis
        y_lim_min = max(ax.get_ylim()[0], 0.0)
        y_lim_max = min(ax.get_ylim()[1], 1.0)
        ax.set_ylim((y_lim_min, y_lim_max))
        ax.set_ylabel(ylabels[li])
        ax.yaxis.grid()  # grid lines
        ax.set_axisbelow(True)  # grid lines are behind the rest

        # Subplot title
        if subtitles:
            ax.set_title(subtitles[li])

    # Set up x axis
    ax = axes[-1]
    ax.set_xlim((x_data[0], x_data[-1]))
    ax.set_xlabel(xlabel)
    ax.set_xticklabels(xticklabels)
    if autofmt_xdate:
        fig.autofmt_xdate()

    # Set up legend
    if legend and '/' in legend:
        ax = axes[int(legend[legend.find('/') + 1:])]
        legend = legend[:legend.find('/')]
    legend_loc = legend if legend else 'best'
    if legend_loc != 'none':
        handles, labels = ax.get_legend_handles_labels()
        # sort legend labels and handles by method order
        labels, handles = zip(*sorted(zip(labels, handles),
                                      key=lambda t: methods.index(t[0])))
        ax.legend(handles, labels, loc=legend_loc, fancybox=True,
                  framealpha=0.5).set_zorder(3)

    # Finalize plot setup
    pylab.tight_layout(pad=0.5, h_pad=0.5, w_pad=0.5, rect=(0, 0, 1, 1))
    for plot_file in plotfs:
        pylab.savefig(plot_file)


def plot_avstats(avstats, fnames):
    """
    Plots antivirus and Hidost true positive counts on a dataset.

    avstats - a dictionary mapping detector name to its TP count
    fnames - where to save the plot (list of file names)
    """
    pylab.figure()
    avstats = sorted(avstats.items(), key=operator.itemgetter(1))
    bar_width = 0.8
    spacing = 0.1
    ax = pylab.gca()

    # Set up y axis
    ax.set_yticks(range(len(avstats)))
    ax.set_yticklabels(map(operator.itemgetter(0), avstats), rotation=0)
    ax.set_ylim((0 - bar_width / 2.0 - spacing,
                 len(avstats) - 1 + bar_width / 2.0 + spacing))

    # Set up x axis
    ax.set_xlabel('True positive count')
    ax.set_xlim((0, avstats[-1][1] * 1.01))  # up to total + 1%
    ax.xaxis.grid()
    ax.set_axisbelow(True)

    # Different colors for AVs, Hidost and Total
    colors = ['#67bc6b'] * len(avstats)  # green for AVs
    colors[-1] = '#a50007'  # red for Total
    for i, (k, v) in enumerate(avstats):
        if k == 'Hidost':
            colors[i] = '#ff767d'  # watermelon color for Hidost

    pylab.barh(range(len(avstats)),
               map(operator.itemgetter(1), avstats),
               bar_width, color=colors, linewidth=0, align='center')
    pylab.tight_layout(pad=0.5, h_pad=0.5, w_pad=0.5, rect=(0, 0, 1, 1))
    if isinstance(fnames, basestring):
        fnames = [fnames]
    for plot_file in fnames:
        pylab.savefig(plot_file)

