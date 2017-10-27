# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Ryan J Ollos <ryan.j.ollos@gmail.com>
# Copyright (C) 2017 Emerson Castaneda <emecas@gmail.com>
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

import unittest


#from trachours.tests.hours import *
#from trachours.tests.ticket import *


def revert_trachours_schema_init(env):
    with env.db_transaction as db:
        db("DROP TABLE IF EXISTS ticket_time")
        db("DROP TABLE IF EXISTS ticket_time_query")
        db("DELETE FROM system WHERE name='trachours.db_version'")


def test_suite():
    suite = unittest.TestSuite()

    import trachours.tests.hours
    suite.addTest(trachours.tests.hours.test_suite())
    import trachours.tests.ticket
    suite.addTest(trachours.tests.ticket.test_suite())
    import trachours.tests.db
    suite.addTest(trachours.tests.db.test_suite())


    return suite


#def load_tests(loader, tests, pattern):
#    return suite()

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
