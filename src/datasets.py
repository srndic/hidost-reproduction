"""
Created on November 17, 2014.
"""

import datetime
import re


def load_dates(infile):
    """
    Parses infile for any dates formatted as YYYY/MM/DD, at most one
    per line. Returns a list of datetime.date objects, in order of
    encounter.
    """
    datere = re.compile(r'\d{4}/\d{2}/\d{2}')
    dates = []
    for line in open(infile, 'rb'):
        match = re.search(datere, line)
        if match:
            dates.append(datetime.date(*(map(int, match.group().split('/')))))
    return dates


def load_SHA256_sums(infile):
    """
    Parses infile for any SHA256 sums (strings of 64 hexadecimal
    characters), at most one per line. Returns them as a list of
    strings, in order of encounter.
    """
    id_re = re.compile(r'[a-fA-F0-9]{64}')
    labels = []
    for line in open(infile, 'rb'):
        match = re.search(id_re, line)
        if match:
            labels.append(match.group())
    return labels
