# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Emerson Castaneda <emecas@gmail.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

user_manual_title = "TracHours Plugin User Manual"
user_manual_version = 1
user_manual_wiki_title = "TracHoursPluginUserManual"
user_manual_content = """
= !TracHours Plugin User Manual =

Track hours spent on tickets

== Description

This plugin helps to keep track of hours worked on tickets. This is an alternative to !TimingAndEstimationPlugin, but with a different approach:

 * Instead of adding hours only via ticket fields, there is a separate view for managing ticket hours. `/hours/<ticket number>` displays the accrued hours for a particular ticket with a timeline-like view, but should also allow adding of new hours (by default, on "today", but this should be changeable via dropdown menus for day, month, year, etc), editing previously entered hours (amount, date, description) and deleting previously allotted hours if you have the appropriate permissions (`TICKET_ADD_HOURS` for your own hours, `TRAC_ADMIN` for the hours of others).
 * A management and query view is at `/hours`. This view displays the hours for all tickets for a given time period (last week, by default) in a way that combines the query interface for querying tickets and the timeline display for hours on the tickets in the time period. Query filters are available to find hours for people, hours for tickets of a certain component, etc.
 * Hours are uniquely assigned to tickets and people.
 * Hours may have a description, which should be displayed in the applicable views; if a description is provided, the hours and description are logged to ticket comments.
 * Tickets have links to `/hours/<ticket number>` as the total hours field so that a user can add and view hours for the ticket.

Hour tracking and estimation is most useful for the following types of questions:

 * How much time has been spent on a project?
 * How much time remains in a budget (estimate for a project)?
 * How much time have we committed to for the next time period?
 * How much time is a developer committed to over the next time period?

If we put hour estimates on tickets, assign tickets to people, associate tickets with milestones, and give milestones due dates, !TracHours can generate reports to answer those questions.

For other Trac time-tracking solutions, see t:TimeTracking.

== Components

!TracHours consists of a number of components that work together to help track time:

=== !TracHoursPlugin

`TracHoursPlugin` is the core component of !TracHours.

 * API function.
 * Navigation bar provider.
 * Query view for `/hours`.
 * Ticket hours view for `/hours/<ticket number>`
 * Stream filter for checking and rendering of estimated hours and total hours fields for tickets
 * RSS feeds at `/hours?format=rss` and `/hours/<ticket number>?format=rss`

This component must be enabled to use the !TracHoursPlugin functionality.

=== !SetupTracHours

`SetupTracHours` sets up the database and custom fields for the !TracHoursPlugin. You must enable this component for anything to work, including the `TracHoursPlugin` component.

=== !TracHoursRoadmapFilter

`TracHoursRoadmapFilter` adds hours information for milestones at `/roadmap` and `/milestone/<milestone name>`

=== !TracHoursSidebarProvider

The `TracHoursSidebarProvider` component uses the !TicketSidebarProviderPlugin (if enabled) to add a form to each ticket for direct addition of hours to the ticket. Hours will be logged as the authenticated user and comments will not be made.

=== !TracHoursByComment

The `TracHoursByComment` component enables adding hours by ticket comments. Comments containing snippets like `5 hours`, `1 hour`, `3.7 hours`, or `0:30 hours` will be added to the total hours for the ticket, provided the commenter has the `TICKET_ADD_HOURS` permission.

=== !MultiprojectHours

The !TracHoursPlugin exports RSS from the `/hours` handler. This has been utilized to provide hours reports across projects sharing the same parent directory. If `trachours.multiproject` is enabled, then `/hours/multiproject` will become a handler front-ending hours reports throughout the project and a link to this will appear on the `/hours` page to `/hours/multiproject`.

The multiproject report breaks down hours by project and worker giving row and column totals. If there are no hours for a project, then that project will not be shown.


"""
