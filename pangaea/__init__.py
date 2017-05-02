# -*- coding: utf-8 -*-
#
#  __init__.py
#  pangaea
#
#  Created by Alan D Snow, 2017.
#  BSD 3-Clause

from .xlsm import LSMGridReader
from .read import open_mfdataset


def version():
    return '0.0.1'


__version__ = version()
