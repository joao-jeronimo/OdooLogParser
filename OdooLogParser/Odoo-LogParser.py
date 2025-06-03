#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, odoo_log_parser, os, sys, importlib

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
    pass

if __name__ == "__main__": exit(Main(exec_name=sys.argv[0], exec_argv=sys.argv[1:]))