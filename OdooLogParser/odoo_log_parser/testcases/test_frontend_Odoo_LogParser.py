#!/bin/env python3
# -*- coding: utf-8 -*-
import unittest, os, importlib, subprocess
from unittest.mock import patch, Mock, MagicMock, call as mocked_call
from odoo_log_parser.testcases import extra_assert
frontend_Odoo_LogParser = importlib.import_module("Odoo-LogParser")

SANDBOX_DIR = '/tmp/unit_testing_Odoo-LogParser/test_frontend_Odoo-LogParser'

class TestcaseFrontendOdooLogParser(unittest.TestCase, extra_assert.ExtraAssert):
    """
    Top-down testing the  frontend.
    """
    
    @patch('builtins.print')
    def test_Main_can_be_called(self, mock_print):
        """
        O método Main() pode ser chamado.
        """
        frontend_Odoo_LogParser.Main("Odoo-LogParser.py", [
            '--logfile', self.odoolog_skels_demo['filename'],
            ])
    
    @patch('builtins.print')
    def test_Main_echoes_test_digest(self, mock_print):
        """
        O frontend tem que aceitar a opção «--test-digest sections», que
        dará o resumo dos testes em forma de secções.
        """
        frontend_Odoo_LogParser.Main("Odoo-LogParser.py", [
            '--logfile', self.odoolog_skels_demo['filename'],
            ])
        # Define what is to be printed:
        lines2beprinted = [
            '===========================================',
            '===== Database: adhoc-test17',
            '===========================================',
            '== Module - hr_payroll_community_demo_data:',
            'Testcase test_skel.TestObjects:',
            '    test_passes: SUCCESS',
            '        Starting TestObjects.test_passes ... ',
            '    test_fails: FAIL',
            '        FAIL: TestObjects.test_fails',
            '            Traceback (most recent call last):',
            '              File "/odoo/Instances/demodevel-jj-hr-odoo17/SuiteRepos/SimplePayslipTemplate/0_Installable/17.0/hr_payroll_community_demo_data/tests/test_skel.py", line 7, in test_fails',
            '                self.assertTrue(False)',
            '            AssertionError: False is not true',
            '             ',
            ]
        # Assert that they were really printed:
        mock_print.assert_has_calls([
                mocked_call(thestring)
                for thestring in lines2beprinted
                ],
            any_order=False)
        self.assertEqual( mock_print.call_count, len(lines2beprinted) )
    
    ############################################################
    ############################################################
    ############################################################
    @classmethod
    def setUpClass(cls):
        cls.odoolog_skels_demo        = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_skels_demo.log') }
        cls.odoolog_with_setup_errors = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_with_setup_errors.log') }
        cls.odoolog_with_test_errors  = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_with_test_errors.log') }
        cls.odoolog_two_succeeded     = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_two_succeeded.log') }
