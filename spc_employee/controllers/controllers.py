# -*- coding: utf-8 -*-
from odoo import http

class Employee(http.Controller):
    @http.route('/spc-employee/employee/', auth='public')
    def index(self, **kw):
        employee = http.request.env['hr.employee'].search([])
        string = ''
        string += '['
        for emp in employee:
            string += '{'
            string += '"id":%s,"name":"%s","position_name":"%s","chief_id":%s' % (str(emp.id), str(emp.name), str(emp.position_id.name), str(emp.chief_id.id))
            string += '},'
        string = string[:-1]
        string += ']'
        string = string.replace('False', 'false')
        return string

    @http.route('/spc-employee/orgchart/', auth='public')
    def iframe(self, **kw):
        return http.request.render('spc_employee.orgchart')
