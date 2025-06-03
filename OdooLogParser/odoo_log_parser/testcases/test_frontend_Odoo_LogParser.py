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
    
    ############################################################
    ############################################################
    ############################################################
    @classmethod
    def setUpClass(cls):
        cls.odoolog_skels_demo        = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_skels_demo.log') }
        cls.odoolog_with_setup_errors = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_with_setup_errors.log') }
        cls.odoolog_with_test_errors  = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_with_test_errors.log') }
        cls.odoolog_two_succeeded     = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_two_succeeded.log') }
