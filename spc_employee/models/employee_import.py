# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import datetime

import base64
import sys
import os

class Import(models.Model):
    _name = 'hr.employee.import'

    def import_employee(self):
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
                # print row
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
            title = self.env['hr.employee.title'].search([('name', '=', arr[6])])
            religion = self.env['hr.employee.religion'].search([('name_th', '=', arr[13])])
            counrty = self.env['res.country'].search([('code', '=', arr[17])])
            race = self.env['res.country'].search([('code', '=', arr[18])])
            # print arr
            # print datetime.now.strftime("%Y")
            obj = {
                'employee_number': arr[0],
                'department_id': department.id,
                'position_id': position.id,
                'status': status.id,
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
                'import': True
            }
            # print obj
            self.env['hr.employee'].sudo().create(obj)

    data = fields.Binary('Import')

# Gender -male -female -other
# blood -a -b -ab -o
# marital -single -married -widower -divorced
