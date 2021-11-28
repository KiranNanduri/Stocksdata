"""Created on Sun Oct 10 06:58:17 2021.

@author: kali
"""

try:
    from .stocksdata import nse
except ModuleNotFoundError():
    print('nse module not found')
