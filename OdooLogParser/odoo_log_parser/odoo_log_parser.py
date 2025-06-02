# -*- coding: utf-8 -*-
import re

RAW_ODOO_LOG_ENTRY_OPENING_REGEX = (
    r"^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2}) (?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2}),(?P<millisecond>[0-9]{3}) (?P<pid>[0-9]+) (?P<log_level>[A-Z]+) (?P<db_name>[A-Za-z0-9_-]+) (?P<logger_name>([A-Za-z_]+)((\.([A-Za-z_]+))*)): "
    )
RAW_ODOO_LOG_ENTRY_BODY_REGEX = (
    r"(?P<log_text>(.|\n)*)$"
    )

class LogEntry:
    def __init__(self, log_map_line, body_regex):
        self.log_map_line = log_map_line
        self.body_regex = body_regex
        self.full_line = log_map_line['full_entry']
        if isinstance(self.body_regex, str): self.body_regex = re.compile(self.body_regex, flags=0)
    
    def __getitem__(self, idx):
        """
        Gets log entry component.
            idx   The component; tipically one of: year, month, day, hour,
                    minute, second, millisecond, pid, log_level, db_name,
                    logger_name or log_text
        """
        # TODO: Automatically find out which fields are present in the opening match.
        if idx not in ['log_text']:
            # Getting fields not present in the body regex is performed by
            # delegating into the opening match:
            return self.log_map_line['opening_match'][idx]
        else:
            # We are caching this:
            cacheline_name = "_cached_"+idx
            result = self.log_map_line.get(cacheline_name, None)
            if not result:
                # Find out how many chars make up part of the opening match:
                opening_match_length = len(self.log_map_line['opening_match'][0])
                # Slice the full entry so that the opening match is removed from it:
                entry_rest = self.full_line[opening_match_length:]
                # Parse it:
                rest_match = self.body_regex.match(entry_rest)
                result = rest_match[idx]
                # Cache the result:
                self.log_map_line[cacheline_name] = result
            # Redirect the indexing instruction into this match:
            return result

class BrowseableConcreteLog:
    """
    A Browseable concrete log represents a logfile that can be browsed
    by entry number or filtered by regex, and that is so because the
    file was somehow parsed into memory.
    It's the job of subclasses to define how this "concretization"
    takes place.
    """

    ############################################################
    #### Index-oriented methods:                        ########
    ############################################################
    def parseEntriesByIdx(self, idx):
        """
        Retrives by index and returns a parsed log entry.
            idx     The (0-based) entry index to retrieve. Entries are returned in
                full, even if they contain newlines.
        """
        # Reparse the joined line:
        return self.entry_list[idx]

    ############################################################
    #### Regex-oriented methods:                        ########
    ############################################################
    def _internal_regex_search(self, regex, string):
        """
        Performs a re.search() call in the way that looks more efficient.
        """
        if isinstance(regex, str):
            return re.search(regex, string, flags=re.MULTILINE)
        else:
            return regex.search(string)

    def parseEntriesByRegexSet(self, regex_set):
        """
        Returns (parsed) entries that match the regex_set list of pairs.
            regex_set   A list of regexes to cumulatively match, inthe form:
                        [ ("field name", regex to match), ]
        Returns a list of parsed entries.
        """
        # Match the entries one by one:
        matching_entries_acc = []
        for lini in range(len(self.entry_list)):
            # Retrieve the full parsed entry:
            full_entry = self.parseEntriesByIdx(lini)
            # Match the clauses one by one:
            does_match = True
            for clause in regex_set:
                # Test the present clause against the line being scanned:
                if not self._internal_regex_search(clause[1], full_entry[clause[0]]):
                    does_match = False
            # See if in the end if does match, and add to acc if so:
            if does_match:
                matching_entries_acc.append( full_entry )
        # Reparse the result:
        return matching_entries_acc

class ParsedLog(BrowseableConcreteLog):
    def __init__(self, source_log, entry_list, source_filter=None):
        self.source_log = source_log
        self.entry_list = entry_list
        self.source_filter = source_filter
    
    def project(self, fieldname, distinct):
        """
        Retrieves a single field from every entry in the log.
        """
        projection = [ entry[fieldname] for entry in self.entry_list ]
        if distinct:
            projection = list(set(projection))
        return projection

    def parseEntriesByRegexSet(self, regex_set):
        """
        Does the browsing and builds a new parsed sublog.
        """
        return ParsedLog(
            source_log      = self.source_log,
            entry_list      = super(ParsedLog, self).parseEntriesByRegexSet(regex_set),
            source_filter   = regex_set,
            )

class PythonLogParser(BrowseableConcreteLog):
    """
    Post-parses a log file and expose it's contents.
    Multiple line may belong to the same log entry. To work around
    this, the parse is parameterized with a regex that is used to
    detect which file lines actually open a new log entry.
    
    Method naming convention:
     * parseEntriesByXpto() - The same as retrieveEntriesByXpto(), but
            the entry/ies are returned in parsed form, as
            dictonary-like objects.
                parseEntriesByIdx()
                parseEntriesByRegexSet()
                parseEntriesByDateRange()
                parseEntriesByEtc()
    """
    
    ############################################################
    #### Initialization:          ##############################
    ############################################################
    def __init__(self, istream, raw_opening_regex=RAW_ODOO_LOG_ENTRY_OPENING_REGEX,
                                raw_body_regex=RAW_ODOO_LOG_ENTRY_BODY_REGEX):
        """
            raw_opening_regex   A string representing a REGEX that matches the opening of
                file lines that begin a new log entry. This regex must match only
                components that will not containe newlines (tipically everything up until
                the entry body).
            raw_body_regex      A string representing a REGEX that matches the rest of the
                log entries; don't forget that on a Python regex the '.' char does not match
                newlines.
        """
        super(PythonLogParser, self).__init__()
        ### Handling and storing the regexes:
        # Assert compiled by us:
        assert isinstance(raw_opening_regex, str)
        assert isinstance(raw_body_regex, str)
        # Compile and store:
        self.opening_regex = re.compile(raw_opening_regex, flags=0)
        self.body_regex = re.compile(raw_body_regex, flags=0)
        self.full_log_entry_regex = re.compile(raw_opening_regex + raw_body_regex, flags=0)
        ### The source stream:
        self.istream = istream
        ### Initalize the parser:
        self.init_parser()

    def init_parser(self):
        """
        Parser initialization read-in the source file and calculates it's entry map.
        """
        ### Read in the file:
        self.istream.seek(0, 0)
        raw_contents = self.istream.read()
        self._splitted_contents = raw_contents.split("\n")
        ### Generate a entry map:
        # An entry map has the the following form (each item of the list describes one log entry):
        #   [{  'lini_start'    : starting line number,
        #       'opening_match' : regex match for the first line of the entry,
        #       'full_entry'    : contents the entry },
        #    {  'lini_start'    : ...,
        #       'opening_match' : ...,
        #       'full_entry'    : ... },
        #    ]
        # Match every line - First element will indicate if an entry begins on that line:
        matched_lines = [
            {  'lini_start'    : linei,
               'opening_match' : self.opening_regex.match(lineconts),
               }
            for (linei, lineconts)
            in enumerate(self._splitted_contents)
            ]
        # Filter-out the lines where an entry does NOT begin:
        beginnings_map = [ item for item in matched_lines if item['opening_match'] ]
        # Also find the end of each entry:
        self.entry_list = []
        for begi in range(len(beginnings_map)):
            # The line where the current entry begins:
            beginning_line = beginnings_map[begi]['lini_start']
            # The line where the current entry ends:
            ending_line = beginnings_map[begi+1]['lini_start'] if len(beginnings_map)>(begi+1) else None
            # Join them:
            this_entry = LogEntry(
                log_map_line = {
                    'lini_start'    : beginnings_map[begi]['lini_start'],
                    'opening_match' : beginnings_map[begi]['opening_match'],
                    'full_entry'    : "\n".join(self._splitted_contents[beginning_line:ending_line]),
                    },
                body_regex = self.body_regex)
            self.entry_list.append(this_entry)

    def parseEntriesByRegexSet(self, regex_set):
        """
        Does the browsing and builds a new parsed sublog.
        """
        return ParsedLog(
            source_log      = self,
            entry_list      = super(PythonLogParser, self).parseEntriesByRegexSet(regex_set),
            source_filter   = regex_set,
            )

    def calcLogLength(self):
        """
        Calculates and returns the current number of log entries.
        """
        return len(self.entry_list)
