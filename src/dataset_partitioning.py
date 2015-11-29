#!/usr/bin/env python
# -*- coding: utf-8 -*-
# dataset_partitioning.py
# Created on March 5, 2015.
"""
Produces a bar plot of dataset partitioning.
"""
from __future__ import print_function

from argparse import ArgumentParser
import operator
import sys

import numpy
import pylab

import plots
from datasets import load_dates


def load_libsvm_labels(f):
    ig0 = operator.itemgetter(0)
    return numpy.array(map(ig0, open(f, 'rb').readlines())).astype('float')


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--train',
                        nargs='+',
                        required=True,
                        help='Training data file(s).')
    parser.add_argument('--test',
                        nargs='+',
                        required=True,
                        help='Test data file(s).')
    parser.add_argument('-l', '--log',
                        action='store_true',
                        help='X-axis log scale.')
    parser.add_argument('--legend',
                        default=False,
                        help='Where to put legend.')
    parser.add_argument('--data-plot',
                        required=True,
                        nargs='*',
                        help='Where to save data quantity plot.')

    args = parser.parse_args()

    print('\nEvaluating data in time periods')
    res = []
    key_dates = []
    all_years = set()
    for w, (f_tr, f_te) in enumerate(zip(args.train, args.test), start=1):
        # Load test data
        y_te = load_libsvm_labels(f_te)
        pos_te, neg_te = (y_te > 0.5).sum(), (y_te < 0.5).sum()

        # Load test dates
        dates = numpy.array(load_dates(f_te))
        week_s, week_e = dates.min(), dates.max()
        key_dates.append(week_s)
        print('Period {} [{} - {}]'.format(w, week_s, week_e))
        all_years.add(str(week_s.year))

        # Load training data
        y_tr = load_libsvm_labels(f_tr)
        pos_tr, neg_tr = (y_tr > 0.5).sum(), (y_tr < 0.5).sum()

        print('Training: {} malicious, {} benign'.format(pos_tr, neg_tr))
        print('Test: {} malicious, {} benign'.format(pos_te, neg_te),
              end='\n\n')
        res.append((pos_tr, neg_tr, pos_te, neg_te))

    pos_tr, neg_tr, pos_te, neg_te = zip(*res)
    print('Dates ranging from {} to {}'.format(key_dates[0], key_dates[-1]))
    print('Total days: {}'.format((key_dates[-1] - key_dates[0]).days + 1))

    print('Plotting training and test sizes')
    bar_width = 0.35
    spacing = 0.05  # spacing between a pair of training/test bars
    xticks = numpy.arange(len(pos_tr)).astype(numpy.float32)

    # Plot
    plots.init_eurasip_style(figure_width=222.5, figure_height=170.0)
    fig = pylab.figure()
    ax = pylab.gca()
    ax.bar(xticks - bar_width - spacing, neg_tr, width=bar_width,
           color='#00691f', linewidth=0, label='Benign training')
    ax.bar(xticks - bar_width - spacing, pos_tr, bottom=neg_tr,
           width=bar_width, color='#a50007', linewidth=0,
           label='Malicious training')
    ax.bar(xticks + spacing, neg_te, width=bar_width, color='#67bc6b',
           linewidth=0, label='Benign evaluation')
    ax.bar(xticks + spacing, pos_te, bottom=neg_te, width=bar_width,
           color='#ff767d', linewidth=0, label='Malicious evaluation')

    # Set up x axis
    ax.set_xticks(xticks)
    ax.set_xticklabels([d.strftime('%b %d') for d in key_dates])
    ax.set_xlim((-2.0 * spacing - bar_width,
                 len(pos_tr) - 1 + 2.0 * spacing + bar_width))
    years_range = sorted(all_years)
    if len(years_range) > 2:
        years_range = [years_range[0], years_range[-1]]
    ax.set_xlabel('Date ({})'.format(' - '.join(years_range)))
    fig.autofmt_xdate()

    # Set up y axis
    pylab.ticklabel_format(axis='y', style='sci', scilimits=(0, 2),
                           useOffset=False)
    ax.yaxis.grid()  # vertical grid lines
    ax.set_axisbelow(True)  # grid lines are behind the rest
    if args.log:
        ax.set_yscale('log')
    ax.set_ylabel('Samples')

    # Set up legend
    legend_loc = args.legend if args.legend else 'best'
    if legend_loc != 'none':
        pylab.legend(loc=legend_loc, fancybox=True, framealpha=0.5)

    # Finalize plot setup
    pylab.tight_layout(pad=0.5, h_pad=0.5, w_pad=0.5, rect=(0, 0, 1, 1))
    for plot_file in args.data_plot:
        pylab.savefig(plot_file)

    return 0


if __name__ == '__main__':
    sys.exit(main())
