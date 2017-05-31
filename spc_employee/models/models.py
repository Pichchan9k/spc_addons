# -*- coding: utf-8 -*-

from odoo import models, fields, api

import sys
import os

# class Division(models.Model):
#     _name = 'hr.division'

#     name = fields.Char('Division Name', required=True)
#     parent_id = fields.Many2one(
#         'hr.department', string='Department', index=True)

#     active = fields.Boolean('Active', default=True)
#     company_id = fields.Many2one('res.company', string='Company',
#                                  index=True, default=lambda self: self.env.user.company_id)
#     note = fields.Text('Note')
#     color = fields.Integer('Color Index')


# class SubDivision(models.Model):
#     _name = 'hr.sub_division'

#     name = fields.Char('Sub Division Name', required=True)
#     parent_id = fields.Many2one('hr.division', string='Division', index=True)

#     active = fields.Boolean('Active', default=True)
#     company_id = fields.Many2one('res.company', string='Company',
#                                  index=True, default=lambda self: self.env.user.company_id)
#     note = fields.Text('Note')
#     color = fields.Integer('Color Index')


class Department(models.Model):
    _inherit = 'hr.department'

    # division_id = fields.Many2many('hr.division', string='Division')
    name_th = fields.Char(string='Department Name Th', require=True)
    code = fields.Char(string='Code', require=True)

    # @api.multi
    # def write(self, vals):
    #     """ If updating manager of a department, we need to update all the employees
    #         of department hierarchy, and subscribe the new manager.
    #     """
    #     # TDE note: auto-subscription of manager done by hand, because currently
    #     # the tracking allows to track+subscribe fields linked to a res.user record
    #     # An update of the limited behavior should come, but not currently
    #     # done.
    #     print '-----vals', vals
    #     if 'manager_id' in vals:
    #         manager_id = vals.get("manager_id")
    #         if manager_id:
    #             manager = self.env['hr.employee'].browse(manager_id)
    #             # subscribe the manager user
    #             if manager.user_id:
    #                 self.message_subscribe_users(user_ids=manager.user_id.ids)
    #         employees = self.env['hr.employee']
    #         for department in self:
    #             employees = employees | self.env['hr.employee'].search([
    #                 ('id', '!=', manager_id),
    #                 ('department_id', '=', department.id),
    #                 ('parent_id', '=', department.manager_id.id)
    #             ])
    #         employees.write({'parent_id': manager_id})
    #     return super(Department, self).write(vals)


class Employee_type(models.Model):
    _name = 'hr.employee.type'

    name = fields.Char('Employee Type')


class Position(models.Model):
    _name = 'hr.position'

    # @api.multi
    # def name_get(self):
    #     res = []
    #     for record in self:
    #         if self._context['lang'] == 'en_US':
    #             res.append((record.id, record.name_en))
    #         else:
    #             res.append((record.id, record.name))
    #     return res

    name = fields.Char(string='Position Eng')
    name_th = fields.Char(string='Position Thai')
    level = fields.Char(string='Level', size=1)
    code = fields.Char(string='Code')

class Status(models.Model):
    _name = 'hr.employee.status'

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = '%s / %s' % (record.name, record.name_th)
            res.append((record.id, name))
        return res

    name = fields.Char(string='Status EN')
    name_th = fields.Char(string='Status TH')

class Provice(models.Model):
    _name = 'spc.address.provice'

    name = fields.Char(string='Provice EN')
    name_th = fields.Char(string='Provice TH')
    pid = fields.Char(string='PID')

class District(models.Model):
    _name = 'spc.address.district'

    name = fields.Char(string='District EN')
    name_th = fields.Char(string='District TH')
    pid = fields.Char(string='PID')
    provice_pid = fields.Char(string='Provice PID')

class Subdistrict(models.Model):
    _name = 'spc.address.subdistrict'

    name = fields.Char(string='Subdistrict EN')
    name_th = fields.Char(string='Subdistrict TH')
    pid = fields.Char(string='PID')
    provice_pid = fields.Char(string='Provice PID')
    district_pid = fields.Char(string='District PID')

class Zipcode(models.Model):
    _name = 'spc.address.zipcode'

    name = fields.Char(string='Zip Code', size=5)

class AddressType(models.Model):
    _name = 'spc.address.type'

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = '%s / %s' % (record.name, record.name_th)
            res.append((record.id, name))
        return res

    name = fields.Char(string='Address Type EN')
    name_th = fields.Char(string='Address Type TH')

class Address(models.Model):
    _name = 'spc.address'

    address_type = fields.Many2one('spc.address.type', string='Address Type')
    addr1 = fields.Char('addr1')
    provice_id = fields.Many2one('spc.address.provice', string='Provice')
    district_id = fields.Many2one('spc.address.district', string='District')
    subdistrict_id = fields.Many2one('spc.address.subdistrict', string='Subdistrict')
    zipcode_id = fields.Many2one('spc.address.zipcode', string='Zip Code')
    phone_number = fields.Integer('Phone Number')
    address_id = fields.Many2one('hr.employee', string='Address Reference', index=True, required=False, ondelete='cascade')


class Religion(models.Model):
    _name = 'hr.employee.religion'

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = '%s / %s' % (record.name, record.name_th)
            res.append((record.id, name))
        return res

    name = fields.Char('Religion EN')
    name_th = fields.Char('Religion TH')


class NameTitle(models.Model):
    _name = 'hr.employee.title'

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = '%s / %s' % (record.name, record.name_th)
            res.append((record.id, name))
        return res

    name = fields.Char('Title')
    name_th = fields.Char('Title Th')


class Employee(models.Model):
    _inherit = 'hr.employee'

    @api.onchange('position_id')
    def on_change_position(self):
        print 'onchange position_id'
        self.level = self.position_id.level

    @api.onchange('title_id')
    def on_change_title(self):
        print 'onchange title', self
        self.title_en = self.title_id.name
        self.title_th = self.title_id.name_th

    title_id = fields.Many2one('hr.employee.title', string='Title', required=True)
    title_en = fields.Char(string='Title En', required=True)
    first_name_en = fields.Char('FirstName En', required=True)
    last_name_en = fields.Char('LastName En', required=True)
    title_th = fields.Char(string='Title Th', required=True)
    first_name_th = fields.Char('FirstName Th', required=True)
    last_name_th = fields.Char('LastName Th', required=True)
    position_id = fields.Many2one('hr.position', string='Position')
    level = fields.Char(string='Level', size=1, stored=True, default='0')
    chief_id = fields.Many2one('hr.employee', string='Chief')
    employee_type = fields.Many2one('hr.employee.type', string='Employee Type')
    status = fields.Many2one('hr.employee.status', string='Status')
    blood_group = fields.Char('Blood Group')
    religion = fields.Many2one('hr.employee.religion', string='Religion')
    citizen_id = fields.Char(string='CitizenID', size=13)
    onboarding_date = fields.Date('Onboarding Date')
    sign_contact_date = fields.Date('Signed Date')
    probation_end_date = fields.Date('ProbationEnd Date')
    start_date = fields.Date('Start Date')
    employee_number = fields.Char(string='Employee ID')
    address_line = fields.One2many('spc.address', 'address_id', string='Address', copy=True)

    @api.onchange('first_name_en', 'last_name_en')
    def some(self):
        self.name = '%s %s' % (self.first_name_en, self.last_name_en)

    # @api.model
    # def create(self, vals):
    #     print 'employee'
    #     # vals['level'] = self.env['hr.position'].search([('id', '=', vals['position_id'])]).level
    #     employee = super(Employee, self).create(vals)
    #     login = '%s.%s@sahapat.co.th' % (employee.first_name_en, employee.last_name_en[0])
    #     res_user = self.env['res.users'].sudo().create({'name': employee.name, 'login': login.lower(), 'password': 123456})
    #     res_user.partner_id.email = login.lower()
    #     employee.user_id = res_user.id
    #     # command = 'python /home/pichchanok/Desktop/odoo10/spc_addons/spc_api/activiti.py ' + str(employee.id)
    #     # os.system(command)
    #     return employee

    def api(self):
        print 'try_api', self
        print self.env['res.users'].search([])

    # @api.model
    # def create(self, vals):
    #     print 'Employee on create -----'
    #     employee = super(Employee, self).create(vals)
    #     create_res_user = self.env['res.users'].sudo().create({'name': employee.name, 'login': employee.name})
    #     print create_res_user
    #     employee.user_id = create_res_user.id
    #     return employee

    # @api.multi
    # def write(self, vals):
    #     vals['level'] = self.env['hr.position'].search([('id','=',vals['position_id'])]).level
    #     return super(Employee, self).write(vals)
