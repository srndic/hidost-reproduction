#!/usr/bin/env python
# -*- coding: utf-8 -*-
# avstats.py
# Created on April 2, 2015.
"""
Produces a bar plot comparing TPRs of antiviruses to Hidost.
"""
from __future__ import print_function

from argparse import ArgumentParser
import pickle
import sys

import plots

def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('res',
                        help='Experiment result (res) file.')
    parser.add_argument('--plot',
                        required=True,
                        nargs='*',
                        help='Where to save plot.')

    args = parser.parse_args()

    print('Loading previous results [{}]'.format(args.res))
    input = pickle.load(open(args.res, 'rb'))
    avstatsl = input['avstats']

    print('Averaging results')
    for i in range(1, len(avstatsl)):
        for av in set(avstatsl[0].keys() + avstatsl[i].keys()):
            avstatsl[0][av] += avstatsl[i][av]
    for av in avstatsl[0].keys():
        avstatsl[0][av] /= float(len(avstatsl))
    avstats = avstatsl[0]

    print('Plotting antivirus detection statistics')
    plots.init_eurasip_style(figure_width=222.5, horizontal=False)
    plots.plot_avstats(avstats, args.plot)
    return 0


if __name__ == '__main__':
    sys.exit(main())
