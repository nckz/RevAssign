#!/Applications/RevAssign.app/Contents/Resources/miniconda/bin/python
# 1. Treat the mpc file as a long string.
# 2. Find and replace a segment of that string with given args.
# 3. Save to a new mpc file.

import os
import sys
import pickle
import xlrd # tools for reading spreadsheets
import xlwt # tools for writing spreadsheets
import PyQt4
from PyQt4 import QtCore,QtGui

usage='usage: '+sys.argv[0] + ''' <input.mpc> <find> <replace>

    Outputs a new mpc file named <input>_replaced.mpc
'''

if ('--help' in sys.argv) or ('-h' in sys.argv):
    print(usage)
    sys.exit(0)

if len(sys.argv) < 4:
    print(usage)
    sys.exit(0)

infile = sys.argv[1]
path = os.path.dirname(infile)
outfile,_ = os.path.splitext(os.path.basename(infile))
outfile = os.path.join(path, outfile+'_replaced.mpc')
search = sys.argv[2]
replace = sys.argv[3]

with open(infile, 'rb') as f:
    p = pickle.load(f)
    s = str(p)
    print '\n'
    print "The number of matching instances of \'{}\': {}".format(search, s.count(search))
    print "Here are the matches:"
    for l in s.split():
        if l.count(search):
            print '\t', l
    print '\n'
    r = s.replace(search, replace)
    d = eval(r,globals(), locals())

    with open(outfile, 'wb') as o:
        print "writing output to: {}".format(outfile)
        pickle.dump(d,o)
