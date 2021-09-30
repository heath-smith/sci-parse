#!user/bin/python
# -*- coding: utf-8 -*-
"""
Test class for csv files.
"""
# import external packages
import time
from unittest.case import TestCase
import numpy as np
from numpy import testing as nptest
import unittest
from pathlib import Path
import sys
import os
import pathlib
import json


# import package
from sparse.parsers import DataFileParser
from sparse.utils import show_plot

class TestReadCsv(unittest.TestCase):

    # set up the test case
    @classmethod
    def setUpClass(cls):
        """
        Setup the test class and initialize test variables
        and expected test results.
        """

        sys.stdout.write('\nSetting up test class... ')

        # path to parent directory
        cls.data_dir = Path(__file__).resolve().parent.parent

        # get the data file field from object
        cls.data_file = os.path.join(
            cls.data_dir, 'test_input' + os.sep + 'dow_moe_rev5_cal_001.csv'
        )

        sys.stdout.write('SUCCESS ')

    def test_is_csv_valid(self):
        """
        Test the _is_csv_valid() method in isolation.
        """

        sys.stdout.write('\n\nTesting _is_csv_valid()...\n')


        # get the file extension, make lowercase
        ext = pathlib.Path(self.data_file).suffix
        ext = ext.lower()

        # open the data file
        with open(self.data_file) as df:

            # new instance of parser class
            test_csv = DataFileParser(f_obj=df, f_type=ext)

            # test _read_csv() method
            test_valid = test_csv._is_csv_valid()

        # assert output is as expected
        self.assertEqual(test_valid, True)

        # plot results for visual check
        #show_plot(test_wv, test_vals)

        sys.stdout.write('\n PASSED')

    def test_read_csv(self):
        """
        Test the _read_csv() method in isolation.
        """

        sys.stdout.write('\n\nTesting _read_csv()...\n')

        # get the file extension, make lowercase
        ext = pathlib.Path(self.data_file).suffix
        ext = ext.lower()

        # open the data file
        with open(self.data_file) as df:

            # new instance of parser class
            test_csv = DataFileParser(f_obj=df, f_type=ext)

            # test _read_csv() method
            test_wv, test_vals = test_csv._read_csv()

        # assert output is as expected
        self.assertGreater(len(test_wv), 0)
        self.assertGreater(len(test_vals), 0)
        self.assertEqual(len(test_wv), len(test_vals))

        # plot results for visual check
        #show_plot(test_wv, test_vals)

        sys.stdout.write('\n PASSED')

    def test_is_valid(self):
        """
        Test is_valid() method for csv files.
        """

        sys.stdout.write('\n\nTesting is_valid()...\n')


        # get the file extension, make lowercase
        ext = pathlib.Path(self.data_file).suffix
        ext = ext.lower()

        # open the data file
        with open(self.data_file) as df:

            # new instance of parser class
            test_csv = DataFileParser(f_obj=df, f_type=ext)

            # test _read_csv() method
            test_valid = test_csv.is_valid()

        # assert output is as expected
        self.assertEqual(test_valid, True)

        sys.stdout.write('\n PASSED')


    def test_read_data(self):
        """
        Test read_data() method for csv files.
        """

        sys.stdout.write('\n\nTesting read_data()...\n')

        # get the file extension, make lowercase
        ext = pathlib.Path(self.data_file).suffix
        ext = ext.lower()

        # open the data file
        with open(self.data_file) as df:

            # new instance of parser class
            test_csv = DataFileParser(f_obj=df, f_type=ext)

            # test _read_csv() method
            test_wv, test_vals = test_csv.read_data()

        # assert output is as expected
        self.assertGreater(len(test_wv), 0)
        self.assertGreater(len(test_vals), 0)
        self.assertEqual(len(test_wv), len(test_vals))

        # plot results for visual check
        #show_plot(test_wv, test_vals)

        sys.stdout.write('\n PASSED')

    @classmethod
    def tearDownClass(cls):

        sys.stdout.write('\nRunning teardown procedure... SUCCESS')

        sys.stdout.close()

if __name__=='__main__':
    unittest.main()
