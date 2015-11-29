#!/usr/bin/env python
# -*- coding: utf-8 -*-
# feat-drift.py
# Created on March 26, 2015.
"""
Plots diffs between feature files for multiple experiments.
"""
from __future__ import print_function

from argparse import ArgumentParser
from collections import OrderedDict
import pickle
import sys

import numpy

import plots


def get_nppf(f_in):
    return open(f_in, 'rb').read().replace('\0\0', '') \
        .replace('\0', '/').split('\n')[1:-1]


def get_pickle(f_in):
    return pickle.load(open(f_in, 'rb'))


def get_feats(f_in):
    try:
        return get_pickle(f_in)
    except:
        try:
            return get_nppf(f_in)
        except:
            print('File {}: unknown format'.format(f_in))
            sys.exit(1)


def print_table(data, stats):
    print('{:<6s}|{:^5s}|{:^11s}|{:^11s}|{:^12s}|{:^5s}'
          .format(*(['Period'] + stats)))
    lf = '{:^6s}|{:>5}|{:>11}|{:>11}|{:>12}|{:>5}'
    nrows = len(data[stats[0]])
    for r in range(nrows):
        fields = ['{}-{}'.format(r, r + 1), data[stats[0]][r]]
        for s in stats[1:4]:
            t = '({:g}%)'.format(round(100.0 * data[s][r] / data[stats[0]][r],
                                       0))
            fields.append('{} {:>6}'.format(data[s][r], t))
        fields.append(data[stats[-1]][r])
        print(lf.format(*fields))


def main():
    stats = ['OLD', 'Add', 'Del', 'Same', 'NEW']
    metric_names = {'Add': 'New features',
                    'Del': 'Obsolete features',
                    'Same': 'Unchanged features'}
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--first',
                        nargs='+',
                        required=True,
                        help='Feature files of the first method.')
    parser.add_argument('--second',
                        nargs='+',
                        required=True,
                        help='Feature files of the second method.')
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
    parser.add_argument('--legend',
                        default=False,
                        help='Where to put legend.')
    parser.add_argument('--plot',
                        required=True,
                        nargs='+',
                        help='Where to save plot.')
    args = parser.parse_args()

    dd = OrderedDict()
    for feats, method in zip((args.first, args.second), args.methods):
        data = []
        for f1, f2 in zip(feats[:-1], feats[1:]):
            l1, l2 = get_feats(f1), get_feats(f2)
            tot_old = len(l1)
            tot_new = len(l2)
            s1, s2 = set(l1), set(l2)
            add = len(s2.difference(s1))
            rem = len(s1.difference(s2))
            same = len(s1.intersection(s2))
            data.append([tot_old, add, rem, same, tot_new])
        dd[method] = dict(zip(stats, [numpy.array(d) for d in zip(*data)]))

    for m, d in dd.iteritems():
        print('{:#^79s}'.format(' {} '.format(m)))
        print_table(d, stats)
        print()

    # Plot setup
    plots.init_eurasip_style(figure_width=222.5,
                         figure_height=265.0,
                         horizontal=len(args.metrics) < 2)
    datas = []
    for metric in args.metrics:
        datas.append([dd[method][metric].astype(numpy.float32) /
                      dd[method][stats[0]]
                      for method in args.methods])
    ylabels = [metric_names[msn] for msn in args.metrics]
    xticklabels = map(str, range(2, len(args.first) + 1))

    plots.sorted_multicomparison(datas=datas,
                                 methods=args.methods,
                                 legend=args.legend,
                                 ylabels=ylabels,
                                 xlabel='Retraining period',
                                 xticklabels=xticklabels,
                                 plotfs=args.plot,
                                 autofmt_xdate=False)
    return 0


if __name__ == '__main__':
    sys.exit(main())

