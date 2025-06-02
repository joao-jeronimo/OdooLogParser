# -*- coding: utf-8 -*-
import re, unittest, random, os
from python_log_parser.testcases.common import PythonLogParser_TestUtils
from unittest import TestCase
from unittest.mock import Mock, MagicMock
from python_log_parser import *

class TestPythonLogParser(unittest.TestCase, PythonLogParser_TestUtils):
    """
    Test behaviour of class PythonLogParser.
    """
    
    def test_begins(self):
        """
        Verified correct creation of testing data.
        """
        self.assertTrue( self.log_file_testing_1['contents'][0].isprintable() )
        self.assertTrue( not self.log_file_testing_1['contents'][0].isspace() )
        self.assertTrue( self.log_file_testing_1['contents'][-1].isprintable() )
        self.assertTrue( not self.log_file_testing_1['contents'][-1].isspace() )
    
    def test_init_from_file_obj(self):
        """
        Tests if the object can be instantiated and that the contents are retrieved from the file.
        """
        with open(self.log_file_testing_1['filename'], "r") as testfile:
            logparser = PythonLogParser(testfile, python_log_parser.RAW_ODOO_LOG_ENTRY_OPENING_REGEX)
            # Test 1st time:
            self.assertEqual( logparser._splitted_contents, self.log_file_testing_1['contents'].split("\n") )
            # Test a 2nd time to ensure cursors were rewound:
            self.assertEqual( logparser._splitted_contents, self.log_file_testing_1['contents'].split("\n") )
    
    def test_calcLogLength(self):
        """
        Method calcLogLength() must return the number of entries (not the number of lines).
        """
        with open(self.log_file_with_multiline_entries_1['filename'], "r") as testfile:
            logparser = PythonLogParser(testfile, python_log_parser.RAW_ODOO_LOG_ENTRY_OPENING_REGEX)
            # Test 1st time:
            self.assertEqual(   logparser.calcLogLength(), 9 )
    
    def test_parseEntriesByIdx_DOT_full_line_WITH_single_lines(self):
        """
        Method parseEntriesByIdx() must refer to the requested entry of the
        file, accessed via full_line member. Case where no entry takes more
        than 1 line.
        """
        with open(self.log_file_testing_1['filename'], "r") as testfile:
            logparser = PythonLogParser(testfile, python_log_parser.RAW_ODOO_LOG_ENTRY_OPENING_REGEX)
            # Test 1st time:
            self.assertEqual(   logparser.parseEntriesByIdx(2).full_line,
                                "2023-10-13 14:22:32,971 201825 INFO sintaf odoo.modules.loading: loading base/security/base_groups.xml" )
            # Test a 2nd time to ensure cursors were rewound:
            self.assertEqual(   logparser.parseEntriesByIdx(2).full_line,
                                "2023-10-13 14:22:32,971 201825 INFO sintaf odoo.modules.loading: loading base/security/base_groups.xml" )
            # Try to get the last entry:
            self.assertEqual(   logparser.parseEntriesByIdx(logparser.calcLogLength()-1).full_line,
                                "2023-10-13 14:22:33,690 201825 INFO sintaf odoo.modules.loading: loading base/views/decimal_precision_views.xml" )
    
    def test_parseEntriesByIdx_DOT_full_line_WITH_multi_lines_get_line_after(self):
        """
        Method parseEntriesByIdx() must refer to the requested entry of the
        file, accessed via full_line member. Case where one of the entries
        before the requested one takes more than 1 line.
        """
        with open(self.log_file_with_multiline_entries_1['filename'], "r") as testfile:
            logparser = PythonLogParser(testfile, python_log_parser.RAW_ODOO_LOG_ENTRY_OPENING_REGEX)
            # Test getting one line:
            self.assertEqual(
                logparser.parseEntriesByIdx(3).full_line,
                "2023-10-13 15:31:36,526 202961 INFO sintaf werkzeug: 192.168.100.25 - - [13/Oct/2023 15:31:36] \"POST /web/dataset/call_kw/mail.channel/channel_seen HTTP/1.0\" 200 - 31 0.019 0.336" )
    
    def test_parseEntriesByIdx_DOT_full_line_WITH_multi_lines_get_big_entry(self):
        """
        Method parseEntriesByIdx() must refer to the requested entry of the
        file, accessed via full_line member. Case where the requested entry
        actually is a multi-line entry.
        """
        with open(self.log_file_with_multiline_entries_1['filename'], "r") as testfile:
            logparser = PythonLogParser(testfile, python_log_parser.RAW_ODOO_LOG_ENTRY_OPENING_REGEX)
            # Test getting one line:
            self.assertEqual(
                logparser.parseEntriesByIdx(1).full_line,
                """2023-10-13 15:31:36,290 202961 ERROR sintaf odoo.sql_db: bad query: UPDATE "mail_channel_partner" SET "write_uid"=2,"seen_message_id"=626,"write_date"=(now() at time zone 'UTC') WHERE id IN (6)
ERROR: could not serialize access due to concurrent update
""" )
    
    def test_parseEntriesByIdx_multi_lines_get_big_entry(self):
        """
        Tests method parseEntriesByIdx() to actually retrieve a parsed multi-line entry.
        """
        with open(self.log_file_with_multiline_entries_1['filename'], "r") as testfile:
            logparser = PythonLogParser(testfile, python_log_parser.RAW_ODOO_LOG_ENTRY_OPENING_REGEX)
            # Test getting one line:
            self.assertEqual( logparser.parseEntriesByIdx(1)['year'], "2023")
            self.assertEqual( logparser.parseEntriesByIdx(1)['month'], "10")
            self.assertEqual( logparser.parseEntriesByIdx(1)['day'], "13")
            self.assertEqual( logparser.parseEntriesByIdx(1)['hour'], "15")
            self.assertEqual( logparser.parseEntriesByIdx(1)['minute'], "31")
            self.assertEqual( logparser.parseEntriesByIdx(1)['second'], "36")
            self.assertEqual( logparser.parseEntriesByIdx(1)['millisecond'], "290")
            self.assertEqual( logparser.parseEntriesByIdx(1)['pid'], "202961")
            self.assertEqual( logparser.parseEntriesByIdx(1)['log_level'], "ERROR")
            self.assertEqual( logparser.parseEntriesByIdx(1)['db_name'], "sintaf")
            self.assertEqual( logparser.parseEntriesByIdx(1)['logger_name'], "odoo.sql_db")
            self.assertEqual( logparser.parseEntriesByIdx(1)['log_text'], """bad query: UPDATE "mail_channel_partner" SET "write_uid"=2,"seen_message_id"=626,"write_date"=(now() at time zone 'UTC') WHERE id IN (6)
ERROR: could not serialize access due to concurrent update
""")
    
    def test_parseEntriesByRegexSet_filters_lines_by_contents__assert_by_string(self):
        """
        Tests method parseEntriesByRegexSet() to filter lines by contents. In this case the assertions are made by string.
        """
        with open(self.log_file_with_multiline_entries_1['filename'], "r") as testfile:
            logparser = PythonLogParser(testfile, python_log_parser.RAW_ODOO_LOG_ENTRY_OPENING_REGEX)
            # Test getting with a filter that matches only one line:
            self.assertEqual(
                logparser.parseEntriesByRegexSet([('log_level', '^ERROR$')]).entry_list[0].full_line,
                """2023-10-13 15:31:36,290 202961 ERROR sintaf odoo.sql_db: bad query: UPDATE "mail_channel_partner" SET "write_uid"=2,"seen_message_id"=626,"write_date"=(now() at time zone 'UTC') WHERE id IN (6)
ERROR: could not serialize access due to concurrent update
""")
            # Test getting with a filter that matches many lines:
            self.assertEqual(
                [ ent.full_line for ent in logparser.parseEntriesByRegexSet([('logger_name', '^odoo_module_writers_lib\..+$')]).entry_list ], [
                    "2023-10-13 15:31:39,015 202961 INFO sintaf odoo_module_writers_lib.domain: ORM domain «('allowed_operating_units_users_ids', '=', False)» translated into «[('operating_unit_id', '=', False), ('allowed_in_operating_unit_ids', '=', False)]».",
                    "2023-10-13 15:31:39,017 202961 INFO sintaf odoo_module_writers_lib.domain: ORM domain «('allowed_operating_units_users_ids', 'in', 2)» translated into «['|', ('operating_unit_id', 'in', [1]), ('allowed_in_operating_unit_ids', 'in', 1)]».",
                    "2023-10-13 15:31:39,041 202961 INFO sintaf odoo_module_writers_lib.domain: ORM domain «('allowed_operating_units_users_ids', '=', False)» translated into «[('operating_unit_id', '=', False), ('allowed_in_operating_unit_ids', '=', False)]».",
                    "2023-10-13 15:31:39,042 202961 INFO sintaf odoo_module_writers_lib.domain: ORM domain «('allowed_operating_units_users_ids', 'in', 2)» translated into «['|', ('operating_unit_id', 'in', [1]), ('allowed_in_operating_unit_ids', 'in', 1)]».",
                ])
            # Test using a filter over the log text:
            self.assertEqual(
                logparser.parseEntriesByRegexSet([('log_text', 'serialize')]).entry_list[0].full_line,
                """2023-10-13 15:31:36,290 202961 ERROR sintaf odoo.sql_db: bad query: UPDATE "mail_channel_partner" SET "write_uid"=2,"seen_message_id"=626,"write_date"=(now() at time zone 'UTC') WHERE id IN (6)
ERROR: could not serialize access due to concurrent update
""")
    
    def test_parseEntriesByRegexSet_filters_lines_by_contents__assert_by_Match_object(self):
        """
        Tests method parseEntriesByRegexSet() to filter lines by contents. In this case the assertions are made by re.Match object.
        """
        with open(self.log_file_with_multiline_entries_1['filename'], "r") as testfile:
            logparser = PythonLogParser(testfile, python_log_parser.RAW_ODOO_LOG_ENTRY_OPENING_REGEX)
            # Test getting with a filter that matches only one line:
            self.assertEqual(
                logparser.parseEntriesByRegexSet([('log_level', '^ERROR$')]).entry_list[0]['log_text'],
                """bad query: UPDATE "mail_channel_partner" SET "write_uid"=2,"seen_message_id"=626,"write_date"=(now() at time zone 'UTC') WHERE id IN (6)
ERROR: could not serialize access due to concurrent update
""")
            # Test getting with a filter that matches many lines:
            self.assertEqual(
                logparser.parseEntriesByRegexSet([('logger_name', '^odoo_module_writers_lib\..+$')]).entry_list[0]['log_text'],
                "ORM domain «('allowed_operating_units_users_ids', '=', False)» translated into «[('operating_unit_id', '=', False), ('allowed_in_operating_unit_ids', '=', False)]»." )
            self.assertEqual(
                logparser.parseEntriesByRegexSet([('logger_name', '^odoo_module_writers_lib\..+$')]).entry_list[1]['log_text'],
                "ORM domain «('allowed_operating_units_users_ids', 'in', 2)» translated into «['|', ('operating_unit_id', 'in', [1]), ('allowed_in_operating_unit_ids', 'in', 1)]»." )
            self.assertEqual(
                logparser.parseEntriesByRegexSet([('logger_name', '^odoo_module_writers_lib\..+$')]).entry_list[2]['log_text'],
                "ORM domain «('allowed_operating_units_users_ids', '=', False)» translated into «[('operating_unit_id', '=', False), ('allowed_in_operating_unit_ids', '=', False)]»." )
            self.assertEqual(
                logparser.parseEntriesByRegexSet([('logger_name', '^odoo_module_writers_lib\..+$')]).entry_list[3]['log_text'],
                "ORM domain «('allowed_operating_units_users_ids', 'in', 2)» translated into «['|', ('operating_unit_id', 'in', [1]), ('allowed_in_operating_unit_ids', 'in', 1)]»." )
    
    ############################################################
    ############################################################
    ############################################################
    @classmethod
    def setUpClass(self):
        self.maxDiff = None
        # Create needed test files:
        self.aux_create_log_file("log_file_testing_1", """
2023-10-13 14:22:31,807 201825 INFO sintaf odoo.modules.loading: loading base/data/res_country_data.xml
2023-10-13 14:22:32,842 201825 INFO sintaf odoo.modules.loading: loading base/data/ir_demo_data.xml
2023-10-13 14:22:32,971 201825 INFO sintaf odoo.modules.loading: loading base/security/base_groups.xml
2023-10-13 14:22:33,391 201825 INFO sintaf odoo.modules.loading: loading base/security/base_security.xml
2023-10-13 14:22:33,552 201825 INFO sintaf odoo.modules.loading: loading base/views/base_menus.xml
2023-10-13 14:22:33,690 201825 INFO sintaf odoo.modules.loading: loading base/views/decimal_precision_views.xml
            """.strip())
        self.aux_create_log_file("log_file_with_multiline_entries_1", """
2023-10-13 15:31:36,274 202963 INFO sintaf longpolling: 192.168.100.25 - - [2023-10-13 15:31:36] "POST /longpolling/poll HTTP/1.0" 200 1311 22.257256
2023-10-13 15:31:36,290 202961 ERROR sintaf odoo.sql_db: bad query: UPDATE "mail_channel_partner" SET "write_uid"=2,"seen_message_id"=626,"write_date"=(now() at time zone 'UTC') WHERE id IN (6)
ERROR: could not serialize access due to concurrent update

2023-10-13 15:31:36,291 202961 INFO sintaf odoo.service.model: SERIALIZATION_FAILURE, retry 1/5 in 0.2029 sec...
2023-10-13 15:31:36,526 202961 INFO sintaf werkzeug: 192.168.100.25 - - [13/Oct/2023 15:31:36] "POST /web/dataset/call_kw/mail.channel/channel_seen HTTP/1.0" 200 - 31 0.019 0.336
2023-10-13 15:31:36,536 202963 INFO sintaf longpolling: 192.168.100.25 - - [2023-10-13 15:31:36] "POST /longpolling/poll HTTP/1.0" 200 513 0.256666
2023-10-13 15:31:39,015 202961 INFO sintaf odoo_module_writers_lib.domain: ORM domain «('allowed_operating_units_users_ids', '=', False)» translated into «[('operating_unit_id', '=', False), ('allowed_in_operating_unit_ids', '=', False)]».
2023-10-13 15:31:39,017 202961 INFO sintaf odoo_module_writers_lib.domain: ORM domain «('allowed_operating_units_users_ids', 'in', 2)» translated into «['|', ('operating_unit_id', 'in', [1]), ('allowed_in_operating_unit_ids', 'in', 1)]».
2023-10-13 15:31:39,041 202961 INFO sintaf odoo_module_writers_lib.domain: ORM domain «('allowed_operating_units_users_ids', '=', False)» translated into «[('operating_unit_id', '=', False), ('allowed_in_operating_unit_ids', '=', False)]».
2023-10-13 15:31:39,042 202961 INFO sintaf odoo_module_writers_lib.domain: ORM domain «('allowed_operating_units_users_ids', 'in', 2)» translated into «['|', ('operating_unit_id', 'in', [1]), ('allowed_in_operating_unit_ids', 'in', 1)]».
            """.strip())
