# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Emerson Castaneda <emecas@gmail.com>
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

import shutil
import tempfile
import unittest

from trac.test import EnvironmentStub
#from trac.ticket.api import TicketSystem
#from trac.ticket.model import Ticket

#from trachours.hours import TracHoursPlugin
from trachours.setup import SetupTracHours
#from trachours.ticket import TracHoursByComment

from trachours.tests import revert_trachours_schema_init

class TracHoursSetupTestCase(unittest.TestCase):
    def setUp(self):
        self.env = EnvironmentStub(default_data=True,
                                   enable=['trac.*', 'trachours.*'])
        self.env.path = tempfile.mkdtemp()
        self.setup = SetupTracHours(self.env)
        with self.env.db_transaction as db:
            self.setup.upgrade_environment(db)

    def tearDown(self):
        self.env.reset_db()
        revert_trachours_schema_init(self.env)
        shutil.rmtree(self.env.path)


    def test_db_version(self):
        db_version = self.setup.db_version
        version = self.setup.version()
        self.assertEquals(db_version,version)

    def test_environtment_needs_upgraded(self):
        ret = self.setup.environment_needs_upgrade()
        self.assertFalse(ret)

    def test_manual_needs_instalation(self):
        ret = self.setup._needs_user_manual()
        self.assertFalse(ret)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TracHoursSetupTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
