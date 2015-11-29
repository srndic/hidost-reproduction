#!/usr/bin/env python
# -*- coding: utf-8 -*-
# method_comparison.py
# Created on March 10, 2015.
"""
Produces a plot comparing different methods on the same dataset.
"""
from __future__ import print_function

from argparse import ArgumentParser
import pickle
import sys

import numpy

import plots


def main():
    metric_names = {'neg_tr': 'Benign training',
                    'pos_tr': 'Malicious training',
                    'neg_te': 'Benign evaluation',
                    'pos_te': 'Malicious evaluation',
                    'acc': 'Accuracy',
                    'AUC': 'Area under ROC',
                    'TPR': 'True positive rate',
                    'FPR': 'False positive rate'}
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--res',
                        nargs='+',
                        required=True,
                        help='Result files of all methods.')
    parser.add_argument('--methods',
                        nargs='+',
                        required=True,
                        help='Names of all methods, in the same '
                        'order as result files.')
    parser.add_argument('--metrics',
                        choices=metric_names.keys(),
                        nargs='+',
                        required=True,
                        help='Which metrics to compare on.')
    parser.add_argument('-l', '--log',
                        action='store_true',
                        help='Plot y-axis using log scale.')
    parser.add_argument('--legend',
                        default=False,
                        help='Where to put legend.')
    parser.add_argument('--plot',
                        required=True,
                        nargs='*',
                        help='Where to save plot(s).')

    args = parser.parse_args()

    assert len(args.res) == len(args.methods), ('There must be an equal '
                                                'number of result and '
                                                'TP files')

    methods = {}
    key_dates = []
    stats = []
    for res_f, method in zip(args.res, args.methods):
        print('Loading results for method {} [{}]'.format(method, res_f))
        input = pickle.load(open(res_f, 'rb'))
        resl = input['res']
        avstatsl = input['avstats']
        key_dates = input['key_dates']
        stats = input['stats']

        print('Averaging results', end='\n\n')
        means = numpy.mean(resl, axis=0)
        means = means.reshape((len(means) / len(stats), len(stats)))
        neg_tr, pos_tr, neg_te, pos_te, acc, AUC, TPR, FPR = zip(*means)
        for i in range(1, len(avstatsl)):
            for av in set(avstatsl[0].keys() + avstatsl[i].keys()):
                avstatsl[0][av] += avstatsl[i][av]
        for av in avstatsl[0].keys():
            avstatsl[0][av] /= float(len(avstatsl))
        avstats = avstatsl[0]
        methods[method] = {'res': dict(zip(stats, zip(*means))),
                           'avstats': avstats}

    print('Dates ranging from {} to {}'.format(key_dates[0], key_dates[-1]))
    print('Total days: {}'.format((key_dates[-1] - key_dates[0]).days + 1))

    # Plot setup
    plots.init_eurasip_style(figure_width=222.5, horizontal=len(args.metrics) < 2)
    ylabels = [metric_names[msn] for msn in args.metrics]
    xticklabels = [d.strftime('%b %d') for d in key_dates]
    years_range = sorted(set([d.strftime('%Y') for d in key_dates]))
    if len(years_range) > 2:
        years_range = [years_range[0], years_range[-1]]
    xlabel = 'Date ({})'.format(' - '.join(years_range))
    datas = []
    for metric in args.metrics:
        datas.append([methods[method]['res'][metric]
                      for method in args.methods])

    plots.sorted_multicomparison(datas=datas,
                                 methods=args.methods,
                                 legend=args.legend,
                                 ylabels=ylabels,
                                 xlabel=xlabel,
                                 xticklabels=xticklabels,
                                 plotfs=args.plot,
                                 autofmt_xdate=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

