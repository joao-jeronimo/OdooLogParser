# -*- coding: utf-8 -*-
import os, random

class OdooLogParser_TestUtils:
    """
    Aux methode for testing the python log parser.
    """
    
    @classmethod
    def aux_create_log_file(self, attrname, contents):
        os.makedirs("/tmp/unit_testing_odoo_log_parser", exist_ok=True)
        fileinfo = {
            'filename'      : "/tmp/unit_testing_odoo_log_parser/TestOdooLogParser-%s-%09d.log" % (attrname, random.random()*1000000000),
            'contents'      : contents,
            }
        with open(fileinfo['filename'], "w") as testfile:
            testfile.write(fileinfo['contents'])
        setattr(self, attrname, fileinfo)
        return fileinfo