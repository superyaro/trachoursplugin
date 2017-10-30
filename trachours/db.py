# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Jeff Hammel <jhammel@openplans.org>
# Copyright (C) 2017 Emerson Castaneda <emecas@gmail.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

from datetime import datetime

from trac.core import Component, implements
from trac.db.schema import Column, Index, Table
from trac.env import IEnvironmentSetupParticipant
from trac.util.datefmt import to_utimestamp, utc
from tracsqlhelper import *

from usermanual import *

# totalhours be a computed field, but computed fields don't yet exist for trac
custom_fields = {
    'estimatedhours': {
        'type': 'text',
        'label': 'Estimated Hours',
        'value': '0'
    },
    'totalhours': {
        'type': 'text',
        'label': 'Total Hours',
        'value': '0'
    }
}


class SetupTracHours(Component):
    implements(IEnvironmentSetupParticipant)

    # IEnvironmentSetupParticipant methods

    db_installed_version = None
    db_version = 4

    def __init__(self):
        self.db_installed_version = self.version()

    def environment_created(self, db=None):
        if self.environment_needs_upgrade():
            self.upgrade_environment()

    def environment_needs_upgrade(self, db=None):
        return self._system_needs_upgrade()

    def _system_needs_upgrade(self):
        return self.db_installed_version < self.db_version

    def upgrade_environment(self, db=None):
        for version in range(self.version(), len(self.steps)):
            for step in self.steps[version]:
                step(self)

        self.env.db_transaction("""
            UPDATE system SET value=%s
            WHERE name='trachours.db_version'
            """, (len(self.steps),))

        self.db_installed_version = len(self.steps)

    def _needs_user_manual(self):
        with self.env.db_transaction as db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT MAX(version) FROM wiki WHERE name=%s
                   """, (user_manual_wiki_title,))

            # rows = self.env.db_query("""
            #        SELECT MAX(version) FROM wiki WHERE name=%s
            #        """, (user_manual_wiki_title,)

            for maxversion in cursor.fetchone():
                maxversion = int(maxversion) \
                    if isinstance(maxversion, (int, long)) \
                    else 0
                break
            else:
                maxversion = 0
        return maxversion < user_manual_version

    def _do_user_man_update(self):
        when = to_utimestamp(datetime.now(utc))
        with self.env.db_transaction as db:
            cursor = db.cursor()
            cursor.execute("""
                    INSERT INTO wiki
                  (name,version,time,author,ipnr,text,comment,readonly)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (user_manual_wiki_title, user_manual_version,
                      when, 'TracHours Plugin', '127.0.0.1',
                      user_manual_content, '', 0,))

    def version(self):
        for value, in self.env.db_query("""
                SELECT value FROM system WHERE name = 'trachours.db_version'
                """):
            return int(value)
        else:
            return 0

    def create_db(self):
        ticket_time_table = Table('ticket_time', key='id')[
            Column('id', auto_increment=True),
            Column('ticket', type='int'),
            Column('time_submitted', type='int'),
            Column('worker'),
            Column('submitter'),
            Column('time_started', type='int'),
            Column('seconds_worked', type='int'),
            Column('comments'),
            Index(['ticket']),
            Index(['worker']),
            Index(['time_started'])]

        create_table(self.env, ticket_time_table)
        execute_non_query(self.env, """
            INSERT INTO system (name, value)
            VALUES ('trachours.db_version', '1')
            """)

    def update_custom_fields(self):
        ticket_custom = 'ticket-custom'
        for name in custom_fields:
            field = custom_fields[name].copy()
            field_type = field.pop('type', 'text')
            if not self.config.get(ticket_custom, field_type):
                self.config.set(ticket_custom, name, field_type)
            for key, value in field.items():
                self.config.set(ticket_custom, '%s.%s' % (name, key), value)
        self.config.save()

    def add_query_table(self):
        time_query_table = Table('ticket_time_query', key='id')[
            Column('id', auto_increment=True),
            Column('title'),
            Column('description'),
            Column('query')]

        create_table(self.env, time_query_table)

    def initialize_old_tickets(self):
        execute_non_query(self.env, """
            INSERT INTO ticket_custom (ticket, name, value)
            SELECT id, 'totalhours', '0' FROM ticket WHERE id NOT IN (
            SELECT ticket FROM ticket_custom WHERE name='totalhours');""")

    def install_manual(self):
        if self._needs_user_manual():
            self._do_user_man_update()

    # ordered steps for upgrading
    steps = [
        [create_db, update_custom_fields],  # version 1
        [add_query_table],  # version 2
        [initialize_old_tickets],  # version 3
        [install_manual],  # version 4
    ]
