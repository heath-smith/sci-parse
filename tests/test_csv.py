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
import json
import plotly.graph_objects as go

# import package
from parsers.parsers import DataFileParser

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

        # data directory + file name
        cls.data_file = (
            'test_input'
            + os.sep
            + 'dow_moe_rev5_cal_001.csv'
        )

        sys.stdout.write('SUCCESS ')

    def test_is_csv_valid(self):
        """
        Test the _is_csv_valid() method in isolation.
        """

        sys.stdout.write('\n\nTesting _is_csv_valid()...\n')

        sys.stdout.write('\n PASSED')

    def test_read_csv(self):
        """
        Test the _read_csv() method in isolation.
        """

        sys.stdout.write('\n\nTesting _read_csv()...\n')

        # new instance of parser class
        test_csv = DataFileParser(self.data_file)

        test_read = test_csv._read_csv()

        sys.stdout.write('\n PASSED')

    def test_is_valid(self):
        """
        Test is_valid() method for csv files.
        """

        sys.stdout.write('\n\nTesting read_data()...\n')

        sys.stdout.write('\n PASSED')


    def test_read_data(self):
        """
        Test read_data() method for csv files.
        """

        sys.stdout.write('\n\nTesting read_data()...\n')

        sys.stdout.write('\n PASSED')

    @classmethod
    def tearDownClass(cls):

        sys.stdout.write('\nRunning teardown procedure... SUCCESS')

        sys.stdout.close()

if __name__=='__main__':
    unittest.main()
