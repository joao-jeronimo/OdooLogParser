#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, odoo_log_parser, os, sys, importlib

def packge2modulename(packagename):
    """
    Converts a python package name into an Odoo module name, that is:
        odoo.addons.my_module_name.teste.test_xpto.py
    ... is converted into:
        my_module_name
    Arguments:
        packagename     The full python package name to convert.
    """
    return packagename.split('.')[2]

def process_test_list(test_list, keys2add):
    """
    Converts a test list as returned by the OdooTestDigest.get_full_test_digest()
    method into a different form.
        test_list   The sublist got with as expression looking like:
                    OdooTestDigest().get_full_test_digest()['dbname']['tests_succeeded']
    Returns a dictionary of dictionaries of dictionaries, looking like:
        {   'module_name_number_one': {
                'test_testcase_one_file_name.TestCaseOneClassName': {
                    'test_method_1_name': {
                        'test_path': "odoo.addons.module_name_number_one.tests.test_testcase_one_file_name.TestCaseOneClassName.test_method_1_name",
                        'test_log': "The log of the test. May be take multiple lines.",
                        **keys2add,
                        },
                    'test_method_2_name': {
                        'test_path': "odoo.addons.module_name_number_one.tests.test_testcase_one_file_name.TestCaseOneClassName.test_method_2_name",
                        'test_log': "The log of the test. May be take multiple lines.",
                        **keys2add,
                        },
                    },
                },
                'test_testcase_two_file_name.TestCaseTwoClassName': {
                    'test_method_1_name': {
                        'test_path': "odoo.addons.module_name_number_one.tests.test_testcase_two_file_name.TestCaseTwoClassName.test_method_1_name",
                        'test_log': "The log of the test. May be take multiple lines.",
                        **keys2add,
                        },
                    'test_method_2_name': {
                        'test_path': "odoo.addons.module_name_number_one.tests.test_testcase_two_file_name.TestCaseTwoClassName.test_method_2_name",
                        'test_log': "The log of the test. May be take multiple lines.",
                        **keys2add,
                        },
                    },
                },
            'module_name_number_two': {
                (...),
                },
            }
    """

def Main(exec_name, exec_argv):
    """
    Program entry-point - Parses the command line arguments and
    invokes corresponding semantics.
        exec_name   The bin name used to call the program.
        exec_argv   Array of program arguments to parse.
    """
    #######################################################
    ##### Configuring the syntax of the cmdline:    #######
    #######################################################
    # Help header:
    parser = argparse.ArgumentParser(description='A parser for Odoo logs.')
    # Named arguments:
    parser.add_argument('--logfile', type=str, default="/dev/stdin",
        help=('An Odoo log file. By default read data from stdin.'))
    # Parsing proper:
    args = parser.parse_args(args=exec_argv)
    
    ###################################################
    ### Main behaviour:     ###########################
    ###################################################
    ### Dump the digest:
    with open(args.logfile, "r") as logfile_obj:
        logparser = odoo_log_parser.OdooTestDigest(logfile_obj)
        digest = logparser.get_full_test_digest()
    ### Convert the digest into our readable form:
    for dbname in digest.keys():
        print(f'===========================================')
        print(f'===== Database: {dbname}')
        print(f'===========================================')
        # Get a list of every module being tested:
        every_module = None
        
        
        #print('== Module - hr_payroll_community_demo_data:')
        #print('Testcase test_skel.TestObjects:')
        #print('    test_fails: FAIL')
        #print('        FAIL: TestObjects.test_fails')
        #print('Traceback (most recent call last):')
        #print('  File "/odoo/Instances/demodevel-jj-hr-odoo17/SuiteRepos/SimplePayslipTemplate/0_Installable/17.0/hr_payroll_community_demo_data/tests/test_skel.py", line 7, in test_fails')
        #print('    self.assertTrue(False)')
        #print('AssertionError: False is not true')
        #print(' ')

if __name__ == "__main__": exit(Main(exec_name=sys.argv[0], exec_argv=sys.argv[1:]))