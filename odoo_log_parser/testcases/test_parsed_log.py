# -*- coding: utf-8 -*-
import re, unittest, random, os
from python_log_parser.testcases.common import PythonLogParser_TestUtils
from unittest import TestCase
from unittest.mock import Mock, MagicMock
from python_log_parser import *

class TestParsedLog(unittest.TestCase, PythonLogParser_TestUtils):
    """
    Test behaviour of class ParsedLog.
    """
    
    def test_project(self):
        """
        Verified correct creation of testing data.
        """
        with open(self.log_file_with_multiline_entries_1['filename'], "r") as testfile:
            # Get every line of any database::
            logparser = PythonLogParser(testfile, python_log_parser.RAW_ODOO_LOG_ENTRY_OPENING_REGEX)
            all_lines = logparser.parseEntriesByRegexSet([('db_name', '^.*$')])
            self.assertEqual( set(all_lines.project('log_level', distinct=True)), {"INFO", "ERROR"})
            self.assertEqual( all_lines.project('db_name', distinct=True), ["sintaf"])
    
    ############################################################
    ############################################################
    ############################################################
    @classmethod
    def setUpClass(self):
        # Create needed test files:
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
