# -*- coding: utf-8 -*-
import re, unittest, random, os
from unittest import TestCase
from unittest.mock import Mock, MagicMock
from python_log_parser import *
from extra_assert import *

class TestOdooTestDigest(unittest.TestCase, ExtraAssert):
    """
    Test behaviour of class OdooTestDigest.
    """
    
    def test_get_full_test_digest_returns_dbnames(self):
        """
        Tests if the test digest includes the db name.
        """
        with open(self.odoolog_skels_demo['filename'], "r") as testfile:
            # Instanciate the parser and try to get the digest:
            logparser = OdooTestDigest(testfile)
            digest = logparser.get_full_test_digest()
            # Assert on digest results:
            self.assertEqual( list(digest.keys()), ["adhoc-test17"])
    
    def test_get_full_test_digest_returns_tests_failing_elements(self):
        """
        Tests if the test digest lists the failing test.
        """
        with open(self.odoolog_skels_demo['filename'], "r") as testfile:
            # Instanciate the parser and try to get the digest:
            logparser = OdooTestDigest(testfile)
            digest = logparser.get_full_test_digest()
            # Assert on digest results:
            self.assertLength( digest["adhoc-test17"]['tests_failing'], 1 )
    
    def test_get_full_test_digest_returns_tests_failing_test_path(self):
        """
        Tests if the test digest includes the test path.
        """
        with open(self.odoolog_skels_demo['filename'], "r") as testfile:
            # Instanciate the parser and try to get the digest:
            logparser = OdooTestDigest(testfile)
            digest = logparser.get_full_test_digest()
            # Assert on digest results:
            self.assertEqual(
                digest["adhoc-test17"]['tests_failing'][0]['test_path'],
                "odoo.addons.hr_payroll_community_demo_data.tests.test_skel.TestObjects.test_fails" )
    
    def test_get_full_test_digest_returns_tests_failing_test_log(self):
        """
        Tests if the test digest includes the test log.
        """
        with open(self.odoolog_skels_demo['filename'], "r") as testfile:
            # Instanciate the parser and try to get the digest:
            logparser = OdooTestDigest(testfile)
            digest = logparser.get_full_test_digest()
            # Assert on digest results:
            self.assertMultilineStringsEqual(
	        	digest["adhoc-test17"]['tests_failing'][0]['test_log'],
	        	"""FAIL: TestObjects.test_fails
Traceback (most recent call last):
  File "/odoo/Instances/demodevel-jj-hr-odoo17/SuiteRepos/SimplePayslipTemplate/0_Installable/17.0/hr_payroll_community_demo_data/tests/test_skel.py", line 7, in test_fails
    self.assertTrue(False)
AssertionError: False is not true
 """ )
    
    def test_get_full_test_digest_returns_setup_errors(self):
        """
        The test digest must include errors that happened inside the setUpClass() method.
        In that case the test_path key will contain the path to the setUpClass() method
        """
        with open(self.odoolog_with_setup_errors['filename'], "r") as testfile:
            # Instanciate the parser and try to get the digest:
            logparser = OdooTestDigest(testfile)
            digest = logparser.get_full_test_digest()
            # Assert on digest results:
            setup_errors = digest["demodevel-jj-hr-odoo13"]['setup_errors']
            self.assertLength( setup_errors, 1 )
            self.assertEqual( setup_errors[0]['test_path'], "odoo.addons.test_simple_payslip_template.tests.test_skel.TestObjects.setUpClass" )
            self.assertMultilineStringsEqual(
	        	setup_errors[0]['test_log'],
	        	"""ERROR: setUpClass (odoo.addons.test_simple_payslip_template.tests.test_skel.TestObjects)
Traceback (most recent call last):
  File "/odoo/Instances/demodevel-jj-hr-odoo13/SuiteRepos/SimplePayslipTemplate/0_Installable/13.0/test_simple_payslip_template/tests/test_skel.py", line 27, in setUpClass
    self.main_company = self.env.ref('base.main_company')
AttributeError: type object 'TestObjects' has no attribute 'env'
 """ )
    
    def test_get_full_test_digest_returns_test_errors(self):
        """
        The test digest must include errors that happened during tests but that do not
        constitute mere assertion failures.
        In that case the test_path key will contain the path to the erroing test, just
        like happened in the case of failures.
        """
        with open(self.odoolog_with_test_errors['filename'], "r") as testfile:
            # Instanciate the parser and try to get the digest:
            logparser = OdooTestDigest(testfile)
            digest = logparser.get_full_test_digest()
            # Assert on digest results:
            tests_errors = digest["demodevel-jj-hr-odoo13"]['tests_errors']
            self.assertLength( tests_errors, 2 )
            # First test:
            self.assertEqual(
                tests_errors[0]['test_path'],
                "odoo.addons.test_simple_payslip_template.tests.test_action_report_simplepayslip.TestActionReportSimplePayslip.test_report_action_created_and_conditioned" )
            self.assertMultilineStringsEqual(
	        	tests_errors[0]['test_log'],
	        	"""ERROR: TestActionReportSimplePayslip.test_report_action_created_and_conditioned
Traceback (most recent call last):
  File "/odoo/releases/13.0/odoo/tools/cache.py", line 85, in lookup
    r = d[key]
  File "/odoo/releases/13.0/odoo/tools/func.py", line 69, in wrapper
    return func(self, *args, **kwargs)
  File "/odoo/releases/13.0/odoo/tools/lru.py", line 44, in __getitem__
    a = self.d[obj].me
KeyError: ('ir.model.data', <function IrModelData.xmlid_lookup at 0x7fc19901e040>, 'action_report_simplepayslip')

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/odoo/Instances/demodevel-jj-hr-odoo13/SuiteRepos/SimplePayslipTemplate/0_Installable/13.0/test_simple_payslip_template/tests/test_action_report_simplepayslip.py", line 12, in test_report_action_created_and_conditioned
    the_repact = self.env.ref('action_report_simplepayslip')
  File "/odoo/releases/13.0/odoo/api.py", line 504, in ref
    return self['ir.model.data'].xmlid_to_object(xml_id, raise_if_not_found=raise_if_not_found)
  File "/odoo/releases/13.0/odoo/addons/base/models/ir_model.py", line 1713, in xmlid_to_object
    t = self.xmlid_to_res_model_res_id(xmlid, raise_if_not_found)
  File "/odoo/releases/13.0/odoo/addons/base/models/ir_model.py", line 1697, in xmlid_to_res_model_res_id
    return self.xmlid_lookup(xmlid)[1:3]
  File "<decorator-gen-25>", line 2, in xmlid_lookup
  File "/odoo/releases/13.0/odoo/tools/cache.py", line 90, in lookup
    value = d[key] = self.method(*args, **kwargs)
  File "/odoo/releases/13.0/odoo/addons/base/models/ir_model.py", line 1683, in xmlid_lookup
    module, name = xmlid.split('.', 1)
ValueError: not enough values to unpack (expected 2, got 1)
 """ )
            # Second test:
            self.assertEqual(
                tests_errors[1]['test_path'],
                "odoo.addons.test_simple_payslip_template.tests.test_printing_payslip.TestPrintingPayslip.test_printing_payslip" )
            self.assertMultilineStringsEqual(
	        	tests_errors[1]['test_log'],
	        	"""ERROR: TestPrintingPayslip.test_printing_payslip
Traceback (most recent call last):
  File "/odoo/Instances/demodevel-jj-hr-odoo13/SuiteRepos/SimplePayslipTemplate/0_Installable/13.0/test_simple_payslip_template/tests/test_printing_payslip.py", line 44, in test_printing_payslip
    self.payslip_01.line_ids.filtered(self.aux_predicate_appears_on_payslip) + 1)
  File "/odoo/releases/13.0/odoo/models.py", line 5653, in __add__
    return self.concat(other)
  File "/odoo/releases/13.0/odoo/models.py", line 5662, in concat
    raise TypeError("Mixing apples and oranges: %s.concat(%s)" % (self, arg))
TypeError: Mixing apples and oranges: hr.payslip.line(1, 3, 4, 5, 6).concat(1)
 """ )
    
    def test_get_full_test_digest_returns_test_sucesses(self):
        """
        The test digest must include tests that succeeded.
        """
        with open(self.odoolog_two_succeeded['filename'], "r") as testfile:
            # Instanciate the parser and try to get the digest:
            logparser = OdooTestDigest(testfile)
            digest = logparser.get_full_test_digest()
            # Assert on digest results:
            tests_errors = digest["demodevel-jj-hr-odoo13"]['tests_succeeded']
            self.assertLength( tests_errors, 3
            )
            # First test:
            self.assertEqual(
                tests_errors[0]['test_path'],
                "odoo.addons.test_simple_payslip_template"
                ".tests.test_action_report_simplepayslip"
                ".TestActionReportSimplePayslip"
                ".test_report_action_created_and_conditioned" )
            self.assertMultilineStringsEqual(
	        	tests_errors[0]['test_log'],
	        	"""Starting TestActionReportSimplePayslip.test_report_action_created_and_conditioned ... """ )
            # Second test:
            self.assertEqual(
                tests_errors[1]['test_path'],
                "odoo.addons.test_simple_payslip_template.tests.test_printing_payslip.TestPrintingPayslip.test_beginnings" )
            self.assertMultilineStringsEqual(
	        	tests_errors[1]['test_log'],
	        	"""Starting TestPrintingPayslip.test_beginnings ... """ )
            # Third test:
            self.assertEqual(
                tests_errors[2]['test_path'],
                "odoo.addons.test_simple_payslip_template"
                ".tests.test_printing_payslip"
                ".TestPrintingPayslip.test_printing_payslip" )
            self.assertMultilineStringsEqual(
	        	tests_errors[2]['test_log'],
	        	"""Starting TestPrintingPayslip.test_printing_payslip ... """ )
    
    
    def test_get_full_test_digest_separates_successes_elements_from_failures(self):
        """
        Digest must not list failing test as success. This might happen
        because successes are gathered from the "Starting" lines.
        """
        with open(self.odoolog_skels_demo['filename'], "r") as testfile:
            # Instanciate the parser and try to get the digest:
            logparser = OdooTestDigest(testfile)
            digest = logparser.get_full_test_digest()
            # Assert that failure is not also miscounted as a success:
            sucks = [é['test_path'] for é in digest["adhoc-test17"]['tests_succeeded']]
            self.assertNotIn(
                "odoo.addons.hr_payroll_community_demo_data."
                "tests.test_skel.TestObjects.test_fails",
                sucks )
            self.assertEqual(sucks[0], 
                "odoo.addons.hr_payroll_community_demo_data."
                "tests.test_skel.TestObjects.test_passes")
            self.assertLength( sucks, 1 )
    def test_get_full_test_digest_separates_successes_elements_from_test_errors(self):
        """
        Digest must not list erroring test as success. This might happen
        because successes are gathered from the "Starting" lines.
        """
        with open(self.odoolog_with_test_errors['filename'], "r") as testfile:
            # Instanciate the parser and try to get the digest:
            logparser = OdooTestDigest(testfile)
            digest = logparser.get_full_test_digest()
            # Assert that failure is not also miscounted as a success:
            sucks = [é['test_path'] for é in digest["demodevel-jj-hr-odoo13"]['tests_succeeded']]
            self.assertNotIn(
                "odoo.addons.test_simple_payslip_template"
                ".tests.test_action_report_simplepayslip"
                ".TestActionReportSimplePayslip"
                ".test_report_action_created_and_conditioned",
                sucks )
            self.assertNotIn(
                "odoo.addons.test_simple_payslip_template"
                ".tests.test_printing_payslip"
                ".TestPrintingPayslip"
                ".test_printing_payslip",
                sucks )
            self.assertEqual(sucks[0],
                "odoo.addons.test_simple_payslip_template"
                ".tests.test_printing_payslip"
                ".TestPrintingPayslip"
                ".test_beginnings")
            self.assertLength( sucks, 1 )
    def test_get_full_test_digest_separates_successes_elements_from_setup_errors(self):
        """
        Digest must not list erroring setups as success. This might happen
        because successes are gathered from the "Starting" lines.
        """
        with open(self.odoolog_with_setup_errors['filename'], "r") as testfile:
            # Instanciate the parser and try to get the digest:
            logparser = OdooTestDigest(testfile)
            digest = logparser.get_full_test_digest()
            # Assert that failure is not also miscounted as a success:
            sucks = [é['test_path'] for é in digest["demodevel-jj-hr-odoo13"]['tests_succeeded']]
            self.assertNotIn(
                "odoo.addons.test_simple_payslip_template."
                "tests.test_skel.TestObjects.setUpClass",
                sucks )
            self.assertLength( sucks, 0 )
    
    ############################################################
    ############################################################
    ############################################################
    @classmethod
    def setUpClass(self):
        # Test digest parsers:
        self.odoolog_skels_demo        = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_skels_demo.log') }
        self.odoolog_with_setup_errors = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_with_setup_errors.log') }
        self.odoolog_with_test_errors  = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_with_test_errors.log') }
        self.odoolog_two_succeeded     = { 'filename': os.path.join(os.path.dirname(__file__), 'fixtures/odoolog_two_succeeded.log') }
