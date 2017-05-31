# -*- coding: utf-8 -*-
from odoo import models, fields, api

import sys
import os

class NameGet:
    def name_get(self, vals):
        print 'name_get: ', self
        print vals
        res = []
        for record in vals:
            if vals._context['lang'] == 'en_US':
                res.append((record.id, record.name))
            else:
                res.append((record.id, record.name_th))
        return res

class Department(models.Model):
    _inherit = 'hr.department'

    # division_id = fields.Many2many('hr.division', string='Division')
    name_th = fields.Char(string='Department Name Th', require=True)
    code = fields.Char(string='Code', require=True)

class Employee_type(models.Model):
    _name = 'hr.employee.type'

    name = fields.Char('Employee Type')


class Position(models.Model):
    _name = 'hr.position'

    @api.multi
    def name_get(self):
        return NameGet().name_get(self)

    name = fields.Char(string='Position Eng')
    name_th = fields.Char(string='Position Thai')
    level = fields.Char(string='Level', size=1)
    code = fields.Char(string='Code')

class Status(models.Model):
    _name = 'hr.employee.status'

    @api.multi
    def name_get(self):
        return NameGet().name_get(self)

    name = fields.Char(string='Status EN')
    name_th = fields.Char(string='Status TH')

class Provice(models.Model):
    _name = 'spc.address.provice'

    @api.multi
    def name_get(self):
        return NameGet().name_get(self)

    name = fields.Char(string='Provice EN')
    name_th = fields.Char(string='Provice TH')
    pid = fields.Char(string='PID')

class District(models.Model):
    _name = 'spc.address.district'

    @api.multi
    def name_get(self):
        return NameGet().name_get(self)

    name = fields.Char(string='District EN')
    name_th = fields.Char(string='District TH')
    pid = fields.Char(string='PID')
    provice_pid = fields.Char(string='Provice PID')

class Subdistrict(models.Model):
    _name = 'spc.address.subdistrict'

    @api.multi
    def name_get(self):
        return NameGet().name_get(self)

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
        return NameGet().name_get(self)

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

class LangaugeNumber(models.Model):
    _name = 'spc.language.name'
        
    name = fields.Char(string='Language')

class LanguageProficency(models.Model):
    _name = 'spc.language.proficency'
    
    name = fields.Char(string='level')

class Language(models.Model):
    _name = 'spc.language'

    name =fields.Many2one('spc.language.name',string='Language')
    speak = fields.Many2one('spc.language.proficency',string='Speak')
    read = fields.Many2one('spc.language.proficency',string='Read/Understand')
    write = fields.Many2one('spc.language.proficency',string='Write')
        

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

class PastJob(models.Model):
    _name = 'hr.employee.pastjob'

    name = fields.Char(string='Present Company',required=True)
    company_address = fields.Char(string='Address')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    first_position = fields.Char(string='First Position',required=True)
    last_poition = fields.Char(string='Last Position',required=True)
    start_salary = fields.Integer(string='Starting Salary')
    final_salary = fields.Integer(string='Final Salary')
    reason = fields.Char(string='Reason For Changing',required=True)

class CarLicense(models.Model):
    _name ='hr.employee.bikelicense'

    name = fields.Char(string='Type')    

class BikeLicense(models.Model):
    _name ='hr.employee.carlicense'

    name = fields.Char(string='Type')         

class References(models.Model):
    _name = 'hr.employee.ref'

    name = fields.Char(string='Name/Surname')
    ref_relationship = fields.Many2one('hr.employee.relation')
    ref_company = fields.Char(string ='Company')
    ref_emp = fields.Boolean(string ='SAHA Employee')
    ref_postion = fields.Char(string ='Position')
    ref_tel = fields.Char(string ='Tel')
    
class ReferencesRelation(object):
    _name = 'hr.employee.relation'

    name =fields.Char(string='Relationship')
                

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

    @api.onchange('citized_id')
    def on_chan_cid(self):
        print 'onchange title', self

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

        # education background
    primary_school = fields.Char(string='Primary School',required=True)
    secondary_school = fields.Char(string='Secondary School',required=True)
    high_school = fields.Char(string='Highy School',required=True)
    colleage = fields.Char(string='College / Vocation',required=True)
    bachelor_degree = fields.Char(string='Bachelor Degree',required=True)
    master_degree = fields.Char(string='Master Degree or Higher',required=True)
    intend_study = fields.Boolean(string='Intend Study')
    intend_where = fields.Char(string='Where?')
    further_study = fields.Char(string='Further Studying at',required=True)
    institute_activity = fields.Char(string=' Activity in The Institute',required=True)
    social_activity = fields.Char(string=' Social Activity',required=True)

    #language skills
    language_skill = fields.One2many('spc.language','name',string='Langauge')

    @api.onchange('first_name_en', 'last_name_en')
    def some(self):
        self.name = '%s %s' % (self.first_name_en, self.last_name_en)

    #special_skills
    thai_typing = fields.Integer(string=' Thai word/minute')
    eng_typing = fields.Integer(string=' English word/minute')
    computer_program = fields.Boolean(string="Computer Program")
    car_license = fields.Many2one('hr.employee.carlicense',string='Car License')
    bike_license = fields.Many2one('hr.employee.bikelicense',string='Bike License')

    # employment record
    past_job = fields.One2many('hr.employee.pastjob','name',string='Record')
    brief = fields.Char(string='Brief Of Duties & Responsibilities in Last Job',required=True)
    ever_worked = fields.Boolean(string="Have you ever working with SAHA GROUP?")
    shift = fields.Boolean(string='Can you work for shift?')
    travel = fields.Boolean(string='Are you willing to travel up country or serve the overseas training?')
    reason_travel = fields.Char(string='Reason') 

    # References
    ref = fields.One2many('hr.employee.ref','name',string='References')

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
