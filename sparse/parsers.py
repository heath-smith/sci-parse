#!user/bin/python
# -*- coding: utf-8 -*-
"""
'parsers.py' contains various file parser classes
used to validate and read data from spectral data
files.
"""

# import dependencies
import csv
import numpy as np


class DataFileParser():
    """
    Class used to parse data files from
    file fields stored in database.
    (Factory Design)
    """

    def __init__(self, f_obj=None, f_type=None, delimiter=',', cols=2):
        """
        Initialize parser class.

        Parameters
        ------------
        f_obj (obj): file object to be read. This can be a
            io.StringIO object or an open() file object.\n
        f_type (str): type of file to be read.\n
        delimiter (str): the type of delimiter to be used on\n
            csv files. `,` is the default.\n
        many (bool): read single or multiple files.
        """

        # initialize file_path class member
        self.file_obj = f_obj
        self.file_type = f_type.lower()
        self.delimiter = delimiter
        self.cols = cols
        self.errors = None
        self.default_message = "No errors found."
        self.x_data = []
        self.y_data = []

    def get_x_data(self):
        """"""
        return self.x_data

    def get_y_data(self):
        """"""
        return self.y_data

    """ reader factory """
    def read_data(self):
        """
        Reads data file and returns the
        spectral data in a 2-D array-like.

        Returns
        ----------
        (callable) the client function that delegates
        which reader to use based on file type.
        """

        # send type to _get_reader client
        reader = self._get_reader(self.file_type)

        # return the reader
        return reader()

    def _get_reader(self, ft):
        """
        Client method delegates which reader to use.

        Parameters
        ----------
        ft (str-like): the type of input file.
        """

        # determine reader to use by ft param
        if 'csv' in ft:
            return self._read_csv
        elif 'jcamp' in ft:
            return self._read_jcamp
        elif 'spa' in ft:
            return self._read_spa
        elif 'json' in ft:
            return self._read_json
        elif 'txt' in ft:
            return self._read_txt
        else:
            raise ValueError(ft)

    """ validator factory """
    def is_valid(self):
        """
        Checks data files before uploading
        to verify contents.

        Returns
        ---------
        (bool) True if file is valid format, False otherwise.
        """

        checker = self._get_valid(self.file_type)

        return checker()

    def _get_valid(self, ft):
        """
        Client method delegates which 'is_valid' method
        to use based on file type.

        Paremeters
        -----------
        ft (str-like): type of input file.
        """
        # determine reader to use by ft param
        if 'csv' in ft:
            return self._is_csv_valid
        elif 'jcamp' in ft:
            return self._is_jcamp_valid
        elif 'spa' in ft:
            return self._is_spa_valid
        elif 'json' in ft:
            return self._is_json_valid
        elif 'txt' in ft:
            return self._is_txt_valid
        else:
            raise ValueError(ft)

    """ begin client readers """
    def _read_csv(self):
        """
        Reads CSV formatted files. Does not
        accept any input parameters.

        Returns
        --------
        `(tuple) (x, y)` where `x` and `y` are arrays with
        `x` being the wavelength, and `y` being the value
        at a particular wavelength.
        """

        x_data = []  # store wavelength values
        y_data = []  # store y-values

        # attempt to open the file
        try:

            # define the csv reader
            rdr = csv.reader(self.file_obj, delimiter=self.delimiter)

            # iterate rows
            for r in rdr:
                try:
                    x_data.append(float(r[0]))
                    y_data.append(float(r[1]))
                except:
                    pass

        except csv.Error as e:

            # raise IOError if exception occurs
            # add logging here
            raise IOError(e)

        self.x_data = x_data
        self.y_data = y_data

        return (x_data, y_data)

    def _read_jcamp(self):
        """
        Reads jcamp formatted files.
        """
        raise NotImplementedError

    def _read_spa(self):
        """
        Reads SPC formatted files.
        """

        f = self.file_obj

        # see lerkoah/spa-on-python on github for explanation #
        # https://github.com/lerkoah/spa-on-python.git #

        f.seek(564)
        points = np.fromfile(f, np.int32, 1)[0]
        print('Points: ', points)

        f.seek(30)
        titles = np.fromfile(f, np.uint8, 255)
        titles = ''.join([chr(x) for x in titles if x != 0])
        print('Titles: ', titles)


        f.seek(576)
        max_wv = np.fromfile(f, np.single, 1)[0]
        min_wv = np.fromfile(f, np.single, 1)[0]
        wv_nums = np.flip(np.linspace(min_wv, max_wv, points))
        print('Wavenumbers: ', wv_nums)

        f.seek(288)
        flag = 0
        while flag != 3:
            flag = np.fromfile(f, np.uint16, 1)

        data_pos = np.fromfile(f, np.uint16, 1)

        f.seek(data_pos[0])

        spectra = np.fromfile(f, np.single, points)
        print('Spectra: ', spectra)

        # scale wv numbers to nanometers
        wv_nums = [1.0E7/x for x in wv_nums]


        self.x_data = wv_nums
        self.y_data = spectra

        return (wv_nums, spectra)

    def _read_json(self):
        """
        Reads JSON formatted files.
        """
        raise NotImplementedError

    def _read_txt(self):
        """
        Reads .txt files. Called by client method.

        Returns
        ----------
        `(tuple) (x, y)` where `x` and `y` are arrays with
        `x` being the wavelength, and `y` being the value
        at a particular wavelength.
        """

        col_1 = []
        col_2 = []
        col_3 = []
        col_4 = []

        rows = self.file_obj.readlines()

        for i, r in enumerate(rows):

            r_strip = r.strip('\n')
            r_split = r_strip.split(self.delimiter)

            try:
                col_1.append(float(r_split[0]))
                col_2.append(float(r_split[1]))

                # read more columns if > 2
                if self.cols == 4:
                    col_3.append(float(r_split[2]))
                    col_4.append(float(r_split[3]))

            except:
                pass

        if self.cols == 2:
            self.x_data = col_1
            self.y_data = col_2

        elif self.cols == 4:

            self.x_data = col_1

            col_2 = np.asarray(col_2)
            col_3 = np.asarray(col_3)
            col_4 = np.asarray(col_4)

            y_vals = (col_4 - col_2) / (col_3 - col_2)
            self.y_data = y_vals.tolist()

        return (self.x_data, self.y_data)

    """ begin client validators """
    def _is_csv_valid(self):
        """
        Check format of .csv and determine
        if valid or not. Does not accept any
        input parameters.

        Returns
        -----------
        (bool) True if valid format, False otherwise.
        """

        self.errors = self.default_message

        header = {}
        x_data = []
        y_data = []

        # attempt to read file object
        try:

            # define the csv reader
            rdr = csv.reader(self.file_obj, delimiter=self.delimiter)

            # iterate rows
            for i, row in enumerate(rdr):

                # check if any rows have more/less than 2 columns
                if len(row) != 2:
                    self.errors = (
                        'File must contain 2 data columns.'
                        + 'Error at line ' + str(i+1) + ' of file.'
                    )
                    return False

                # separate header strings from data floats
                try:
                    x_data.append(float(row[0]))
                    y_data.append(float(row[1]))
                except:
                    header[str(row[0]).lower()] = str(row[1]).lower()


            # check header for wavelength column
            wave = False
            for h in header.keys():
                if 'wavelength' in h:
                    wave = True
                    break

            # if no wavelength col found,
            # return false
            if not wave:
                self.errors = (
                    'No wavelength column found.'
                )
                return False

            # return false if x/y data lengths
            # do not match
            if len(x_data) != len(y_data):
                self.errors = (
                    'X and Y column lengths do not match.'
                )
                return False

        except csv.Error as e:

            # If exception occurs, return false
            # and set the error message
            self.errors = str(e)
            return False

        return True

    def _is_jcamp_valid(self):
        """
        """
        raise NotImplementedError

    def _is_spa_valid(self):
        """
        Determines if .spa file is valid. Does
        not accept any input parameters.

        Returns
        -----------
        (bool) True if valid, False otherwise.
        """

        f = self.file_obj

        # see lerkoah/spa-on-python on github for explanation #
        # https://github.com/lerkoah/spa-on-python.git #

        try:
            f.seek(564)
            points = np.fromfile(f, np.int32, 1)[0]

            f.seek(30)
            titles = np.fromfile(f, np.uint8, 255)
            titles = ''.join([chr(x) for x in titles if x != 0])

            f.seek(576)
            max_wv = np.fromfile(f, np.single, 1)[0]
            min_wv = np.fromfile(f, np.single, 1)[0]
            wv_nums = np.flip(np.linspace(min_wv, max_wv, points))

            f.seek(288)
            flag = 0
            while flag != 3:
                flag = np.fromfile(f, np.uint16, 1)

            data_pos = np.fromfile(f, np.uint16, 1)

            f.seek(data_pos[0])

            spectra = np.fromfile(f, np.single, points)

            if len(wv_nums) != len(spectra):
                self.errors = 'Data arrays must have equal length.'
                return False

        except Exception as e:
            self.errors = str(e)
            return False

        return True

    def _is_json_valid(self):
        """
        """
        raise NotImplementedError

    def _is_txt_valid(self):
        """
        Checks the format of a .txt file to ensure
        it is valid. Does not accept any input parameters.

        Returns
        ------------
        (bool) True if file format is valid, False otherwise.
        """

        self.errors = self.default_message

        header = {}
        x_data = []
        y_data = []

        try:
            rows = self.file_obj.readlines()

            for i, r in enumerate(rows):

                r_strip = r.strip('\n')
                r_split = r_strip.split(self.delimiter)


                try:
                    x_data.append(float(r_split[0]))
                    y_data.append(float(r_split[1]))
                except:
                    header[i+1] = (
                        ' '.join(r_split)
                        if isinstance(r_split, list)
                        else str(r_split)
                    )

            if len(x_data) != len(y_data):
                self.errors = "Data arrays not equal."
                return False

            if len(x_data) == 0 or len(y_data) == 0:
                self.errors = "Data arrays must have length > 0."
                return False

        except Exception as e:
            self.errors = str(e)
            return False

        return True
