##
# Copyright 2012-2014 The Cyprus Institute
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
Support for PGI as toolchain compiler.

@author: George Tsouloupas (The Cyprus Institute)
"""

import easybuild.tools.systemtools as systemtools
from easybuild.tools.toolchain.compiler import Compiler


class Pgi(Compiler):
    """PGI compiler class"""

    COMPILER_MODULE_NAME = ['PGI']

    COMPILER_FAMILY = "PGI"
    COMPILER_UNIQUE_OPTS = {
                            'loop': (False, "Automatic loop parallellisation"),
                            'f2c': (False, "Generate code compatible with f2c and f77"),
                            'lto':(False, "Enable Link Time Optimization"),
                            }
    COMPILER_UNIQUE_OPTION_MAP = {
                                  'i8': 'fdefault-integer-8',
                                  'r8': 'fdefault-real-8',
                                  'unroll': 'funroll-loops',
                                  'f2c': 'ff2c',
                                  'loop': ['ftree-switch-conversion', 'floop-interchange',
                                            'floop-strip-mine', 'floop-block'],
                                  'lto':'flto',
                                  'optarch':'march=native',
                                  'openmp':'fopenmp',
                                  'strict': ['mieee-fp', 'mno-recip'],
                                  'precise':['mno-recip'],
                                  'defaultprec':[],
                                  'loose': ['mrecip', 'mno-ieee-fp'],
                                  'veryloose': ['mrecip=all', 'mno-ieee-fp'],
                                  }

    COMPILER_OPTIMAL_ARCHITECTURE_OPTION = {
                                            systemtools.INTEL : 'march=native',
                                            systemtools.AMD : 'march=native'
                                           }

    COMPILER_CC = 'gpcc'
    COMPILER_CXX = 'pgg++'
    COMPILER_C_UNIQUE_FLAGS = []

    COMPILER_F77 = 'pgf77'
    COMPILER_F90 = 'pgfortran' """pgf90?"""
    COMPILER_F_UNIQUE_FLAGS = ['f2c']

    LIB_MULTITHREAD = ['pthread']
    LIB_MATH = ['m']

    def _set_compiler_vars(self):
        super(Pgi, self)._set_compiler_vars()

        if self.options.get('32bit', None):
            self.log.raiseException("_set_compiler_vars: 32bit set, but no support yet for " \
                                    "32bit PGI in EasyBuild")

        # to get rid of lots of problems with libgfortranbegin
        # or remove the system gcc-gfortran
        # also used in eg LIBBLAS variable
        self.variables.nappend('FLIBS', "gfortran", position=5)

        # append lib dir paths to LDFLAGS (only if the paths are actually there)
        # Note: hardcode 'GCC' here; we can not reuse COMPILER_MODULE_NAME because
        # it can be redefined by combining GCC with other compilers (e.g., Clang).
        pgi_root = self.get_software_root('PGI')[0]
        self.variables.append_subdirs("LDFLAGS", pgi_root, subdirs=["lib64", "lib"])
