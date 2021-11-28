"""nse module.

@author: KiranN.
@Version: 0.1
"""

import os
import logging
import requests
from concurrent import futures
from zipfile import ZipFile
from datetime import date


class nse():
    """Download NSE daily stock data.

    Download daily bhav copies i.e., stock trade details from nse webstie.
    bhavCopyDownload takes in start year/mmth and end year/mmth and loops in
    to download all the daily files between the dates provided.
    """

    today = date.today()
    current_mmth = int(today.strftime("%m"))
    current_year = int(today.strftime("%Y"))

    def __init__(self):

        self.days = list(range(1, 32))
        self.urladdr = "https://www1.nseindia.com/content/historical/EQUITIES/"
        self.file = "bhav.csv.zip"

    @staticmethod
    def __counter(val=1):
        """Counter to increment and track for looping.

        when input value is 'reset', Resent count to 0.
        """
        while True:
            check = yield val

            if check == 'reset':
                val = 0
            else:
                val += 1

    @staticmethod
    def __consoleHandler():
        """Streamhandler to display processing info to console.

        Function to Intialize streamhandler if not present
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        format_str = '%(levelname)s - %(asctime)s - %(name)s - %(message)s'

        formatter = logging.Formatter(format_str, style='%')

        if not len(logger.handlers):

            consolehandler = logging.StreamHandler()
            consolehandler.setLevel(logging.INFO)
            consolehandler.setFormatter(formatter)
            logger.addHandler(consolehandler)

        return logger

    @staticmethod
    def __threading(func, _list):
        """Threading to download files in parallel.

        Takes in function and list as inputs to map and execute in parallel.
        """
        with futures.ThreadPoolExecutor() as executor:
            executor.map(func, _list)

    @staticmethod
    def __fileDownload(file):
        """Use requests module with download modules from Nse site.

        Takes in http path as input and download the file to local.
        """
        file = file
        saveto = savepath

        filename = file.split('/')[-1]
        download = requests.get(file, timeout=2)

        if download.status_code == 200:

            filename_path = saveto + '/' + filename

            open(filename_path, 'wb').write(download.content)

            with ZipFile(filename_path, 'r') as zip:
                zip.extractall(path=saveto)

            os.remove(filename_path)

    def bhavCopyDownload(self, start_year=current_year,
                         start_mnth=current_mmth, end_year=current_year,
                         end_mmth=current_mmth,
                         saveto=os.path.expanduser('~')):
        """Download bhav copy zip files from nse website.

        :param start_year: file download start year. Default to current_year.
        :param start_mnth: files download start mmth. Defaults to current_mmth.
        :param end_year: file download end year. Defaults to current year.
        :param end_mmth: file download end mmth. Default to current_mmth.
        :param saveto: path to save downloaded files. Default to working dir.
        """
        global savepath
        savepath = saveto
        mmth_gen = self.__counter(int(start_mnth))
        year_gen = self.__counter(int(start_year))
        mmth, year = next(mmth_gen), next(year_gen)
        _logger = self.__consoleHandler()

        while True:

            downloaddateformat = date(year, mmth, 1)
            yyyy = int(downloaddateformat.strftime("%Y"))
            mm = int(downloaddateformat.strftime("%m"))
            mon = downloaddateformat.strftime("%h")

            if os.access(saveto, os.R_OK) is False:
                print("No write access to '{}' so exiting, correct path"
                      .format(savepath))
                break

            url_path = "".join([self.urladdr, str(yyyy), '/',
                                mon.upper(), '/'])

            filesurl = ["".join([url_path, 'cm', str(day).zfill(2),
                                 str(mon).upper(),
                                 str(yyyy), self.file])
                        for day in self.days]

            _logger.info(f"Downloding for {yyyy} and {mon} to path {savepath}")

            # Start Download Process till curennt day, month reached.

            if yyyy < end_year:

                if mm < 12:

                    self.__threading(self.__fileDownload, filesurl)
                    mmth = next(mmth_gen)

                else:

                    self.__threading(self.__fileDownload, filesurl)
                    year = next(year_gen)
                    mmth_gen.send('reset')
                    mmth = next(mmth_gen)

            elif yyyy == end_year and mm < end_mmth:

                self.__threading(self.__fileDownload, filesurl)
                mmth = next(mmth_gen)

            elif yyyy == end_year and mm == end_mmth:

                self.__threading(self.__fileDownload, filesurl)

                _logger.info("Downloaded from year {} - mmth {} till year {} - mmth {}".format(start_year, mm, yyyy, mm))

                break

            else:

                _logger.info('Check start_year and end_years passed')
                break
