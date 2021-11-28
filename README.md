#### NSE BhavCopy Download

Download daily Bhavcopy stock data from NSE webstite.

Installtion steps:

PyPI:

pip install stocksdata

Git:

python -m pip install -e git+https://github.com/KiranNanduri/StockCode.git#egg=stocksdata

#### Usage

import stocksdata

nse = stocksdata.nse()


##### Pass optional parameters. By default will download current month files and  save files to home directory.

nse.downloadBhavCopy(saveto = <path>, start_year = <download start year>, start_month = 'download start month',
			end_year = <download end year>, end_month = <download end month>
			)
