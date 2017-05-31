# -*- coding: utf-8 -*-

from odoo import models, fields, api

class onboarding_calendar(models.Model):
    _name = 'onboarding.calendar'

    name = fields.Char(string='Name', required=True)
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    description = fields.Text()
    calendar_event = fields.Many2one('calendar.event', string='Event')
    parent_event = fields.Many2one('calendar.event')
    
    # filter
    department = fields.Many2one('hr.department', string='Department')
    division = fields.Many2one('hr.division', string='Division')
    sub_division = fields.Many2one('hr.sub_division', string='Sub Division')
    level = fields.Many2one('hr.employee.level', string='Level')

    # exclude
    exclude_department = fields.Many2one('hr.department', string='Department')
    exclude_division = fields.Many2one('hr.division', string='Division')
    exclude_sub_division = fields.Many2one('hr.sub_division', string='Sub Division')
    exclude_level = fields.Many2one('hr.employee.level', string='Level')

class onboarding_event(models.Model):
    _inherit = 'calendar.event'

    event_onboarding = fields.Many2many('onboarding.calendar', string='On Boarding')
    event_attendees = fields.Many2many('calendar.event.attendee', string='Attendees')

class event_attendee(models.Model):
    _name = 'calendar.event.attendee'

    name = fields.Many2one('hr.employee', string='Employee')
    check_in = fields.Datetime('Check In')
    check_out = fields.Datetime('Check Out')