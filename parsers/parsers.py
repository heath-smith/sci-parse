"""
'parsers.py' contains various file parser classes
used to validate and read data from spectral data
files stored in the database.
"""

# import dependencies
import csv, json, io, pathlib
from django.core.files.storage import default_storage

class DataFileParser():
    """
    Class used to parse data files from
    file fields stored in database.
    (Factory Design)
    """

    def __init__(self, fp=None, many=False):
        """
        Initialize parser class.

        Parameters
        ------------
        fp (path): path of data file.
        """

        # initialize file_path class member
        self.file_path = fp

    def read_data(self):
        """
        Reads data file and returns the
        spectral data in a 2-D array-like.
        """

        # get the file extension
        ext = pathlib.Path(self.file_path.name).suffix

        # send type to _get_reader client
        reader = self._get_reader(ext.lower())

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
        else:
            raise ValueError(ft)


    def is_valid(self):
        """
        Checks data files before uploading
        to verify contents.

        Returns
        ---------
        (bool) True if file is valid format, False otherwise.
        """

        return True

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
        else:
            raise ValueError(ft)

    def _read_csv(self):
        """
        Reads CSV formatted files.
        """

        wv = []  # store wavelength values
        val = []  # store y-values

        # attempt to open the file
        try:
            # open the file object
            f = default_storage.open(
                self.file_path.name
            ).read().decode('utf-8')

            # define the csv reader
            rdr = csv.reader(
                io.StringIO(f),
                delimiter=','
            )

            # iterate rows
            for r in rdr:
                try:
                    wv.append(float(r[0]))
                    val.append(float(r[1]))
                except:
                    pass

        except csv.Error as e:

            # raise IOError if exception occurs
            # add logging here
            raise IOError(e)

        return (wv, val)

    def _read_jcamp(self):
        """
        Reads jcamp formatted files.
        """

    def _read_spa(self):
        """
        Reads SPC formatted files.
        """

    def _read_json(self):
        """
        Reads JSON formatted files.
        """

    def _is_csv_valid(self):
        """
        """

    def _is_jcamp_valid(self):
        """
        """

    def _is_spa_valid(self):
        """
        """

    def _is_json_valid(self):
        """
        """


