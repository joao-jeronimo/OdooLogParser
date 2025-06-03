#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, odoo_log_parser, os, sys, importlib

def packge2modulename(packagename):
    """
    Converts a python package name into an Odoo module name, that is:
        odoo.addons.my_module_name.teste.test_xpto.TestXpto.test_name
    ... is converted into:
        my_module_name
    Arguments:
        packagename     The full python package name to convert.
    """
    return packagename.split('.')[2]
def packge2testcasename(packagename):
    """
    Converts a python package name into a testcase name, that is:
        odoo.addons.my_module_name.teste.test_xpto.TestXpto.test_name
    ... is converted into:
        test_xpto.TestXpto
    Arguments:
        packagename     The full python package name to convert.
    """
    return '.'.join( packagename.split('.')[4:6] )
def packge2testname(packagename):
    """
    Converts a python package name into the test method name, that is:
        odoo.addons.my_module_name.teste.test_xpto.TestXpto.test_name
    ... is converted into:
        test_name
    Arguments:
        packagename     The full python package name to convert.
    """
    return packagename.split('.')[-1]

def process_test_report(test_dict, keys2add={}):
    """
    Converts a test list as returned by the OdooTestDigest.get_full_test_digest()
    method into a different form.
        test_dict   The sublist got with as expression looking like:
                    OdooTestDigest().get_full_test_digest()['dbname']
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
    test_list = [
        *[  {   **li,
                'result': 'tests_succeeded'
                }
            for li in test_dict['tests_succeeded']
            ],
        *[  {   **li,
                'result': 'tests_failing'
                }
            for li in test_dict['tests_failing']
            ],
        *[  {   **li,
                'result': 'tests_errors'
                }
            for li in test_dict['tests_errors']
            ],
        ]
    # Get a list of modules in the list:
    modules_in_list = list({
        packge2modulename(one_test['test_path'])
        for one_test in test_list
        })
    # For each of them, process:
    ret_dict = dict()
    for module in modules_in_list:
        # Add the module key:
        ret_dict[module] = dict()
        # Every test of this module:
        this_mod_tests = [
            one_test
            for one_test in test_list
            if packge2modulename(one_test['test_path']) == module
            ]
        # Get a list of testcases:
        testcases_in_list = list({
            packge2testcasename(one_test['test_path'])
            for one_test in this_mod_tests
            })
        # For each of them, process:
        for testcase in testcases_in_list:
            # Every test of this module:
            this_mod_tests = [
                one_test
                for one_test in test_list
                if packge2modulename(one_test['test_path']) == module
                ]
            # Add the key with it's list:
            ret_dict[module][testcase] = {
                packge2testname(testee['test_path']): {   **testee,
                    **keys2add,
                    }
                for testee in this_mod_tests
                }
    # Return the result:
    return ret_dict

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
        # Convert the lists:
        converted_tests = process_test_report(digest[dbname])
        # List if all modules with no repetitions:
        all_modules_names = list( converted_tests.keys() )
        # Report each module:
        for modname in all_modules_names:
            print(f'== Module - {modname}:')
            # Report each module's testcase:
            for testcase_name, testcase_tests in converted_tests[modname].items():
                print(f'Testcase {testcase_name}:')
                # Report each testcase's tests:
                for test_name, test_information in testcase_tests.items():
                    # Convert the result into a shiny format:
                    shiny_result = {
                        'tests_succeeded'   : 'SUCCESS',
                        'tests_failing'     : 'FAIL',
                        'tests_errors'      : 'ERROR',
                        }[ test_information["result"] ]
                    # Print the test header:
                    print(f'    {test_name}: {shiny_result}')
                    # Print the test output log:
                    for log_line in test_information["test_log"].split('\n'):
                        print(f'        {log_line}')

if __name__ == "__main__": exit(Main(exec_name=sys.argv[0], exec_argv=sys.argv[1:]))