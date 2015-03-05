"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

#'includes': ['sip','xlrd','xlwt','atexit','PyQt4', 'PyQt4.QtCore', 'PyQt4.QtGui'], \

#'excludes': ['PyQt4.QtDesigner', 'PyQt4.QtNetwork', 'PyQt4.QtOpenGL', 'PyQt4.QtScript', 'PyQt4.QtSql', 'PyQt4.QtTest', 'PyQt4.QtWebKit', 'PyQt4.QtXml', 'PyQt4.phonon']}

from setuptools import setup

APP = ['RevAssign.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': False, \
           'includes': ['sip','xlrd','xlwt','PyQt4', 'PyQt4.QtCore', 'PyQt4.QtGui']}
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
