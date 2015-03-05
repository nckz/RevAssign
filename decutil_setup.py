'''
A C/C++ extension module that implements a RevAssign sorting method.
    
    To make issue the following command:
        $ python <name>_setup.py build_ext --inplace
'''
__author__  = "Nicholas Zwart"
__date__    = "2011dec31"

from distutils.core import setup, Extension

Module1 = Extension('decutil', # this name must have an init<name> function defined.
    #define_macros = [('MAJOR_VERSION', '1'),('MINOR_VERSION', '0')],
    include_dirs = ['/usr/include'],
    libraries = ['c'],
    library_dirs = ['/usr/lib','.'],
    sources = ['decutil.cpp'])

setup (name = 'general reconstruction libs',
    version = '1.0',
    description = 'Speed up sorting in RevAssign.',
    author = 'Nicholas Zwart',
    url = 'http://www.ismrm.org/12/7T.pdf',
    long_description = '''
    Speed up sorting in RevAssign by a lot.
    ''',
    ext_modules=[Module1])
