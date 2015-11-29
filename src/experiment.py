#!/usr/bin/env python
# -*- coding: utf-8 -*-
# experiment.py
# Created on January 14, 2015.
"""
"""
from __future__ import print_function

from argparse import ArgumentParser
import collections
import pickle
import shelve
import sys
import warnings

import numpy
import pylab
from sklearn import datasets, metrics
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.svm import SVC

import plots
from datasets import load_dates, load_SHA256_sums

###############################################################################
# code snippet, to be included in 'sitecustomize.py'
import sys

def info(typet, value, tb):
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
        # we are in interactive mode or we don't have a tty-like
        # device, so we call the default hook
        sys.__excepthook__(typet, value, tb)
    else:
        import traceback, pdb
        # we are NOT in interactive mode, print the exception...
        traceback.print_exception(typet, value, tb)
        print
        # ...then start the debugger in post-mortem mode.
        pdb.pm()

sys.excepthook = info
###############################################################################


def experiment_stats(y_tr, y_te, y_pr, y_val):
    cm = metrics.confusion_matrix(y_te, y_pr)
    print('      TRUE  FALSE')
    print('POS {tp:>6} {fp:>6}'.format(tp=cm[1][1], fp=cm[0][1]))
    print('NEG {tn:>6} {fn:>6}'.format(tn=cm[0][0], fn=cm[1][0]))

    neg_tr, neg_te = len(numpy.where(y_tr < 0.5)[0]), cm[0][1] + cm[0][0]
    assert len(numpy.where(y_te < 0.5)[0]) == neg_te
    print('Negatives: train {}; test {}'.format(neg_tr, neg_te))
    pos_tr, pos_te = len(numpy.where(y_tr > 0.5)[0]), cm[1][1] + cm[1][0]
    assert len(numpy.where(y_te > 0.5)[0]) == pos_te
    print('Positives: train {}; test {}'.format(pos_tr, pos_te))

    TPR = float(cm[1][1]) / pos_te
    FPR = float(cm[0][1]) / neg_te

    acc = metrics.accuracy_score(y_te, y_pr)
    print('Accuracy:', acc)

    fprs, tprs, _ = metrics.roc_curve(y_te, y_val)
    AUROC = metrics.auc(fprs, tprs)
    print('AUROC:', AUROC)
    return numpy.array([neg_tr, pos_tr, neg_te, pos_te, acc, AUROC, TPR, FPR])


def perform_experiment(train_fs, test_fs, avstats_in, binarize,
                       classifier='RF', subsample=False):
    print('Performing experiment')
    res = []
    key_dates = []
    avstats = collections.defaultdict(int)
    for w, (f_tr, f_te) in enumerate(zip(train_fs, test_fs), start=1):
        # Load test dates
        dates = numpy.array(load_dates(f_te))
        week_s, week_e = dates.min(), dates.max()
        key_dates.append(week_s)
        print('\nPeriod {} [{} - {}]'.format(w, week_s, week_e))

        # Load training data
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            X_tr, y_tr = datasets.load_svmlight_file(f_tr)
        print(X_tr.shape)
        if subsample:
            new_size = int(round(X_tr.shape[0] * subsample))
            subsam = numpy.random.choice(X_tr.shape[0], new_size)
            X_tr = X_tr[subsam, :]
            y_tr = y_tr[subsam]
        if binarize:
            X_tr.data = numpy.ones_like(X_tr.data)
        X_tr = X_tr.toarray()

        # Train classifier
        if classifier == 'RF':
            clf = RFC(n_estimators=200, n_jobs=1 if subsample else -1)
        elif classifier == 'SVM':
            clf = SVC(kernel='rbf', gamma=0.0025, C=12)
        sample_weight = None
        print('Training set size: {}'.format(X_tr.shape))
        clf.fit(X_tr, y_tr, sample_weight=sample_weight)
        tr_n_feats = X_tr.shape[1]
        del X_tr

        # Load and classify test data
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            X_te, y_te = datasets.load_svmlight_file(f_te, n_features=tr_n_feats)
        if binarize:
            X_te.data = numpy.ones_like(X_te.data)
        X_te = X_te.toarray()
        print('Test set size: {}'.format(X_te.shape))
        y_pr = clf.predict(X_te)
        if classifier == 'RF':
            y_val = clf.predict_proba(X_te)[:, 1]
        elif classifier == 'SVM':
            y_val = clf.decision_function(X_te)
        del X_te

        # Evaluate experimental results
        res.append(experiment_stats(y_tr, y_te, y_pr, y_val))

        # Load file IDs
        fileIDs = numpy.array(
            load_SHA256_sums(f_te))[numpy.where(y_te > 0.5)]

        # Update AV detection results
        for fid in fileIDs:
            avstats['Total'] += 1
            if fid in avstats_in:
                for av, det in avstats_in[fid]['report'].iteritems():
                    if det:
                        avstats[av] += 1
        del fileIDs
        avstats['Hidost'] += numpy.logical_and(y_te == y_pr, y_te > 0.5).sum()
    res = numpy.concatenate(res)
    return res, key_dates, avstats


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
    parser.add_argument('-c', '--count',
                        type=int,
                        default=1,
                        required=True,
                        help='How many times to perform the experiment.')
    parser.add_argument('-s', '--avstats',
                        required=True,
                        help='Python shelve file with antivirus '
                        'detection data.')
    parser.add_argument('--binarize',
                        default=False,
                        action='store_true',
                        help='Turn on to use binary features.')
    parser.add_argument('--res-out',
                        default=False,
                        help='Where to save pickle file with '
                        'all results/statistics.')
    parser.add_argument('--classifier',
                        default='RF',
                        choices=['RF', 'SVM'],
                        help='Classifier (RF or SVM)')
    parser.add_argument('--subsample',
                        default=False,
                        type=float,
                        help='Training set subsampling percentage')

    args = parser.parse_args()
    assert len(args.train) == len(args.test), ('There must be an equal '
                                               'number of training and '
                                               'test files')
    if args.subsample:
        assert args.subsample > 0.0 and args.subsample <= 1.0
    resl = []
    avstatsl = []
    key_dates = []
    print('Loading antivirus detection data')
    avstats_in = shelve.open(args.avstats)
    print('Running {} experiments'.format(args.count))
    for i in range(1, args.count + 1):
        print('\n\n{:#^79s}'.format(' Experiment {} '.format(i)))
        res, key_dates, avstats = perform_experiment(args.train,
                                                     args.test,
                                                     avstats_in,
                                                     args.binarize,
                                                     args.classifier,
                                                     args.subsample)
        resl.append(res)
        avstatsl.append(avstats)
    resl = numpy.vstack(resl)
    avstats_in.close()
    if args.res_out:
        print('Saving results [{}]'.format(args.res_out))
        output = {'res': resl,
                  'avstats': avstatsl,
                  'key_dates': key_dates,
                  'stats': ['neg_tr', 'pos_tr', 'neg_te', 'pos_te',
                            'acc', 'AUC', 'TPR', 'FPR']}
        pickle.dump(output, open(args.res_out, 'wb+'))

    print('Averaging results')
    means = numpy.mean(resl, axis=0)
    weeks = len(args.train)
    means = means.reshape((weeks, len(means) / weeks))
    neg_tr, pos_tr, neg_te, pos_te, acc, AUC, TPR, FPR = zip(*means)
    for i in range(1, len(avstatsl)):
        for av in set(avstatsl[0].keys() + avstatsl[i].keys()):
            avstatsl[0][av] += avstatsl[i][av]
    for av in avstatsl[0].keys():
        avstatsl[0][av] /= float(len(avstatsl))
    avstats = avstatsl[0]
    del resl, means, weeks, avstatsl

    print('Dates ranging from {} to {}'.format(key_dates[0], key_dates[-1]))
    print('Total days: {}'.format((key_dates[-1] - key_dates[0]).days + 1))

    return 0


if __name__ == '__main__':
    sys.exit(main())

