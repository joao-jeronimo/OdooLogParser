# -*- coding: utf-8 -*-

# Library version control:
#  2024-05-22 - Initial version.

import re, unittest
from unittest import TestCase

class ExtraAssert:
    money_decimal_places = 2
    
    # For numbers and other non-objects:
    def assertZero(self, num):
        self.assertEqual( 0, num )
    def assertIsNone(self, obj):
        self.assertTrue( obj is None )
    def assertIsFalse(self, obj):
        self.assertTrue( obj is False )
    def assertMoneyEqual(self, one, other):
        """
        Asserts that two amounts expressing money are equal after
        being rounded for `money_decimal_places` decimal places.
        """
        self.assertEqual(   round(one, self.money_decimal_places),
                            round(other, self.money_decimal_places))
    
    # For collections:
    def assertLength(self, collection, thelen, msg=None):
        self.assertEqual( len(collection), thelen, msg=(msg or "Length of this collection is not %d: %s"%(
            thelen, repr(collection), ) ) )
    def assertEmpty(self, collection, is_odoo_record=False, msg=None):
        self.assertLength( collection, 0, msg=(msg or ("Collection is not empty: %s" % 
            repr(collection if not is_odoo_record else collection.mapped('display_name') ))) )
    def assertNotEmpty(self, collection, msg=None):
        self.assertGreater( len(collection), 0, msg=(msg or ("Collection is empty: %s"%repr(collection))))
    
    def assertSingleton(self, collection, msg=None):
        self.assertLength( collection, 1, msg=(msg or ("Collection %s is not a singleton" % collection)) )
    def assertCorrectOrder(self, collection, can_one_appear_before_other, elem_to_str):
        """
        Assert that a coolection is in the correct oreder.
        can_one_appear_before_other     Predicate that returnas true if its first arg is
                                        supposed to appear before its the second arg.
        """
        for i in range(len(collection)-1):
            one   = collection[i]
            other = collection[i+1]
            self.assertTrue(
                can_one_appear_before_other(one, other),
                "Collection %s (or %s) is out of other: %s should appear before %s." % (
                    str(collection),
                    str([elem_to_str(colleem) for colleem in collection]),
                    elem_to_str(one),
                    elem_to_str(other),
                    )
                )
    
    def assertAnyFits(self, collection, predicate, is_odoo_record=False, msg=None):
        """
        Asserts that at least one element of the colection fits a given predicate.
        """
        fittings = [
            colitem
            for colitem in collection
            if predicate(colitem)
            ]
        self.assertNotEmpty(fittings, msg=(msg or ("No collection item fits the predicate: %s" % repr(collection if not is_odoo_record else collection.mapped('display_name')) )))
    
    def assertEveryFits(self, collection, predicate, is_odoo_record=False, msg=None):
        """
        Asserts that every element of the colection fits a given predicate.
        """
        non_fittings = [
            colitem
            for colitem in collection
            if not predicate(colitem)
            ]
        self.assertEmpty(non_fittings, msg=(msg or ("The following collection items don't fit the predicate: %s" %
            repr(non_fittings if not is_odoo_record else non_fittings.mapped('display_name')) )))
    
    # For strings:
    def assertIsSubstring(self, whole_string, substring):
        """
        Asserts that the first argument contains the second argument as a substring.
            whole_string    String to search on.
            substring       The string that we assert that is a substring of whole_string.
        """
        self.assertEqual( type(whole_string), str )
        self.assertEqual( type(substring), str )
        self.assertNotEqual( len(substring), 0 )
        self.assertTrue(
                substring in whole_string,
                msg="String «%s» is not a substring of «%s»." % (substring, whole_string, ) )
    
    def assertStringContains(self, the_string, to_search):
        """
        Asserts that the first argument contains at least one of the elements
        of the second argument.
            the_string      String to search on.
            to_search       List of strings.
        """
        self.assertNotEqual( the_string, False )
        self.assertEqual( type(the_string), str )
        self.assertNotEqual( len(the_string), 0 )
        lowered = the_string.lower()
        self.assertTrue(
                any([ (tf in lowered) for tf in to_search ]),
                msg="String %s contains none of the strings: %s" % (lowered, repr(to_search), ) )
    def assertStringNotContains(self, the_string, to_search):
        """
        Asserts that the first argument contains none of the elements of the
        second argument.
            the_string      String to search on.
            to_search       List of strings.
        """
        lowered = the_string.lower()
        for tf in to_search:
            self.assertFalse( tf in lowered )
    def assertMultilineStringsEqual(self, one, other, linewise_strip=False):
        # Assert their types:
        self.assertEqual(type(one), str)
        self.assertEqual(type(other), str)
        # Split the strings:
        one_splitted = one.split('\n')
        other_splitted = other.split('\n')
        # Assert lines equal line by line:
        for lini in range(min(len(one_splitted), len(other_splitted))):
            # Build comparable lines:
            comparable_oneline = one_splitted[lini]
            comparable_otherline = other_splitted[lini]
            if linewise_strip:
                comparable_oneline      = comparable_oneline.strip()
                comparable_otherline    = comparable_otherline.strip()
            # Do assert that they are equal:
            self.assertEqual(comparable_oneline, comparable_otherline, msg=("Multiline strings differ at line %d" % lini))
        # Whole comparisons can be performed only if theere is no linewise strip:
        if not linewise_strip:
            # Assert same number of lines:
            self.assertEqual(len(one_splitted), len(other_splitted), msg=("The strings have a different number of lines.") )
            # Finally, assert that the string as a whole equals:
            self.assertEqual(one, other)
