# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import datetime

import base64
import sys
import os

class ImportLine(models.Model):
    _name = 'hr.employee.importline'

    name = fields.Char('Displayname')
    employee_number = fields.Char('Employee Number')
    department_id = fields.Many2one('hr.department', string='Department')
    position_id = fields.Many2one('hr.position', string='Position')
    status_id = fields.Many2one('hr.employee.status', string='Status')
    sign_contact_date = fields.Date('SignDate')
    probation_end_date = fields.Date('ProbationEndDate')
    title_id = fields.Many2one('hr.employee.title', string='Prefix')
    first_name_en = fields.Char('FnameEng')
    last_name_en = fields.Char('LnameEng')
    first_name_th = fields.Char('FnameTh')
    last_name_th = fields.Char('LnameTh')
    gender = fields.Char('Gender')
    citizen_id = fields.Char('CitizenID')
    religion = fields.Many2one('hr.employee.religion', string='Religion')
    marital = fields.Char('Marital')
    birthday = fields.Date('Birthday')
    blood_group = fields.Char('Bloodgroup')
    country_id = fields.Many2one('res.country', string='Country')
    race_id = fields.Many2one('res.country', string='Race')
    login = fields.Char('Loginame')
    domain = fields.Char('Domain')

    import_ref = fields.Many2one('hr.import.employee')
    status = fields.Selection([('success', 'Success'), ('fail', 'Fail')], string='Status')

class Import(models.Model):
    _name = 'hr.import.employee'

    def import_employee(self):
        print self
        csv = base64.decodestring(self.data)
        head = csv[:csv.index('\n') - 1]
        data = csv[csv.index('\n') + 1:]
        while data != '':
            if data.find('\n') == -1:
                row = data
                data = ''
            else:
                row = data[:data.index('\n') - 1]
                data = data[data.index('\n') + 1:]
            arr = []
            while row != '':
                if row.find(',') == -1:
                    vals = row
                    row = ''
                else:
                    vals = row[:row.index(',')]
                    row = row[row.index(',') + 1:]
                arr.append(vals)
            department = self.env['hr.department'].search([('code', '=', arr[1])])
            position = self.env['hr.position'].search([('code', '=', arr[2])])
            status = self.env['hr.employee.status'].search([('name_th', '=', arr[3])])
            print 'status -------', status.id
            title = self.env['hr.employee.title'].search([('name', '=', arr[6])])
            religion = self.env['hr.employee.religion'].search([('name_th', '=', arr[13])])
            counrty = self.env['res.country'].search([('code', '=', arr[17])])
            race = self.env['res.country'].search([('code', '=', arr[18])])
            obj = {
                'employee_number': arr[0],
                'department_id': department.id,
                'position_id': position.id,
                'status_id': status.id,
                'sign_contact_date': '03-12-2017',
                'probation_end_date': '03-12-2017',
                'title_id': title.id,
                'first_name_en': arr[7],
                'last_name_en': arr[8],
                'first_name_th': arr[9],
                'last_name_th': arr[10],
                'gender': arr[11],
                'citizen_id': arr[12],
                'religion': religion.id,
                'marital': arr[14],
                'birthday': '03-12-2017',
                'blood_group': arr[16].lower(),
                'country_id': counrty.id,
                'race_id': race.id,
                'name': '%s %s' % (arr[7], arr[8]),
                'level': position.level,
                'nick_name_th': '',
                'nick_name_en': '',
                'onboarding_date': '03-12-2017',
                'login': arr[19],
                'domain': arr[20],
                'import_ref': self.id,
                'status': 'fail'
            }
            # self.env['hr.employee'].sudo().create(obj)
            import_line = self.env['hr.employee.importline'].sudo().create(obj)
            self.write({'success_row': [(4, import_line.id)]})

    def action_import(self):
        print 'action_import'

    def action_confirm(self):
        print 'action_confirm'
        self.state = 'confirm'

    def action_cancel(self):
        print 'action_cancel'
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        import_employee = super(Import, self).create(vals)
        import_employee.name = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return import_employee

    name = fields.Char('Displayname')
    data = fields.Binary('Import')
    success_row = fields.One2many('hr.employee.importline', 'import_ref', string='Success', domain=[('status', '=', 'success')])
    fail_row = fields.One2many('hr.employee.importline', 'import_ref', string='Fail', domain=[('status', '=', 'fail')])
    state = fields.Selection([('draft', 'Draft'), ('import', 'Imported'), ('confirm', 'Confirmed'), ('cancel', 'Cancelled')], string='State', default='draft')
    desc = fields.Text('Description')
