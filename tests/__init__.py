# -*- coding: utf-8 -*-
"""

    Tests

    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import unittest
import doctest


def suite():
    suite = unittest.TestSuite()
    suite.addTests(doctest.DocFileSuite(
        '../README.rst', encoding='utf-8',
        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    )
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
