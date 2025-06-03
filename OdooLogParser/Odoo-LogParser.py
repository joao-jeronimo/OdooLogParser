#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, odoo_log_parser, os, sys, importlib

def packge2modulename(packagename):
    pass

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
        #print('/odoo/Instances/demodevel-jj-hr-odoo17/SuiteRepos/SimplePayslipTemplate/0_Installable/17.0/hr_payroll_community_demo_data/tests/test_skel.py:')
        #print('    test_fails: FAIL')
        #print('        FAIL: TestObjects.test_fails')
        #print('Traceback (most recent call last):')
        #print('  File "/odoo/Instances/demodevel-jj-hr-odoo17/SuiteRepos/SimplePayslipTemplate/0_Installable/17.0/hr_payroll_community_demo_data/tests/test_skel.py", line 7, in test_fails')
        #print('    self.assertTrue(False)')
        #print('AssertionError: False is not true')
        #print(' ')

if __name__ == "__main__": exit(Main(exec_name=sys.argv[0], exec_argv=sys.argv[1:]))