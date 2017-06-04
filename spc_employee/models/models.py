# -*- coding: utf-8 -*-
from odoo import models, fields, api

import sys
import os

class NameGet:
    def name_get(self, vals):
        res = []
        for record in vals:
            if vals._context['lang'] == 'en_US':
                res.append((record.id, record.name))
            else:
                res.append((record.id, record.name_th))
        return res

class Department(models.Model):
    _inherit = 'hr.department'

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
    addr1 = fields.Char('Address')
    provice_id = fields.Many2one('spc.address.provice', string='Provice')
    district_id = fields.Many2one('spc.address.district', string='District')
    subdistrict_id = fields.Many2one('spc.address.subdistrict', string='Subdistrict')
    zipcode_id = fields.Many2one('spc.address.zipcode', string='Zip Code')
    phone_number = fields.Integer('Phone Number')
    address_id = fields.Many2one('hr.employee', string='Address Reference', index=True, required=False, ondelete='cascade')

class LangaugeNumber(models.Model):
    _name = 'spc.language.name'
        
    name = fields.Char(string='Language')

class LanguageSkill(models.Model):
    _name = 'spc.language.skill'

    def level(self):
        return [('fair','Fair'),('good','Good'),('excellent','Excellent')]

    name = fields.Many2one('spc.language.name', string='Language')
    speak = fields.Selection(level, string='Speak')
    read = fields.Selection(level, string='Read')
    write = fields.Selection(level, string='Write')
    ref_id = fields.Many2one('hr.employee', string='Language skil Reference', index=True, required=False, ondelete='cascade')


class Institue(models.Model):
    _name = 'spc.institute'

    name = fields.Char(string='Institute', required=True)

class Education(models.Model):
    _name = 'spc.employee.edu'

    level_of_education = fields.Char('Level')
    institute = fields.Many2one('spc.institute', string='Instutue')
    institute_type = fields.Selection([('domestic', 'Domestic'), ('abroad', 'Abroad')], string='Institute Type', required=True)
    major = fields.Char(string='Major', required=True)
    gpa = fields.Float(string='G.P.A.')
    start_study = fields.Date(string='From')
    end_study = fields.Date(string='To')
    education_id = fields.Many2one('hr.employee', string='Education Reference', index=True, required=False, ondelete='cascade')


class Religion(models.Model):
    _name = 'hr.employee.religion'

    @api.multi
    def name_get(self):
        return NameGet().name_get(self)

    name = fields.Char('Religion EN')
    name_th = fields.Char('Religion TH')


class NameTitle(models.Model):
    _name = 'hr.employee.title'

    @api.multi
    def name_get(self):
        return NameGet().name_get(self)

    name = fields.Char('Title')
    name_th = fields.Char('Title Th')

class PastJob(models.Model):
    _name = 'hr.employee.pastjob'
    _order = 'start_date'

    name = fields.Char(string='Company', required=True)
    company_address = fields.Char(string='Address', required=True)
    company_type = fields.Selection([('sahagroup', 'Saha Group'), ('present', 'Present'), ('past','Past')], default='no' , string='Type')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    first_position = fields.Char(string='First Position', required=True)
    last_poition = fields.Char(string='Last Position', required=True)
    start_salary = fields.Integer(string='Starting Salary', required=True)
    final_salary = fields.Integer(string='Final Salary', required=True)
    reason_for_leave = fields.Char(string='Reason For Changing', required=True)
    pastjob_id = fields.Many2one('hr.employee', string='Pastjob Reference', index=True)

class CarLicense(models.Model):
    _name ='hr.employee.bikelicense'

    name = fields.Char(string='Type')    

class BikeLicense(models.Model):
    _name ='hr.employee.carlicense'

    name = fields.Char(string='Type')         

class References(models.Model):
    _name = 'hr.employee.ref'

    name = fields.Char(string='Name')
    company = fields.Char(string ='Company')
    relationship = fields.Char(string ='Relatonship')
    ref_type = fields.Selection([('ref','References'),('saha_group','Saha Group'),('not_family','Not is family')], string ='Type')
    postion = fields.Char(string ='Position')
    tel = fields.Char(string ='Tel')
    ref_id = fields.Many2one('hr.employee', string='Persons Reference', index=True)

class Children(models.Model):
    _name = 'hr.employee.children'
    
    name = fields.Char()
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Sex', required=True)
    age = fields.Char('Age', required=True)
    education_level = fields.Char('Education Level', required=True)
    children_id = fields.Many2one('hr.employee', string='Children Ref', index=True, required=False, ondelete='cascade')

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

    @api.onchange('first_name_en', 'last_name_en')
    def some(self):
        self.name = '%s %s' % (self.first_name_en, self.last_name_en)

    title_id = fields.Many2one('hr.employee.title', string='Title', required=True)
    title_en = fields.Char('Title En', required=True)
    title_th = fields.Char('Title Th', required=True)
    first_name_en = fields.Char('Name', required=True)
    last_name_en = fields.Char('Surname', required=True)
    first_name_th = fields.Char('Name Thai', required=True)
    last_name_th = fields.Char('Surname Thai', required=True)
    nick_name_en = fields.Char('Nickname', required=True)
    nick_name_th = fields.Char('Nickname Thai', required=True)
    position_id = fields.Many2one('hr.position', string='Position')
    level = fields.Char('Level', size=1, stored=True, default='0')
    chief_id = fields.Many2one('hr.employee', string='Chief')
    employee_type = fields.Many2one('hr.employee.type', string='Employee Type')
    status = fields.Many2one('hr.employee.status', string='Status')
    blood_group = fields.Char('Blood Group')
    religion = fields.Many2one('hr.employee.religion', string='Religion')
    citizen_id = fields.Char('CitizenID', size=13)
    onboarding_date = fields.Date('Onboarding Date')
    sign_contact_date = fields.Date('Signed Date')
    probation_end_date = fields.Date('ProbationEnd Date')
    start_date = fields.Date('Start Date')
    employee_number = fields.Char(string='Employee ID')
    address_line = fields.One2many('spc.address', 'address_id', string='Address', copy=True)

    #children
    children_line = fields.One2many('hr.employee.children', 'children_id', string='No. of Children', copy=True)

    # education background
    education = fields.One2many('spc.employee.edu','education_id', string='Education Background')
    intend_further_study = fields.Selection([('no', 'No'), ('yes', 'Yes'), ('domestic', 'Domestic'), ('abroad', 'Abroad')], string='Intend to further study')
    studying_at = fields.Many2one('spc.institute', string='Studying at')
    studying_major = fields.Char(string='Major')
    studying_year_of_end = fields.Char(string='Year of graduation', limit=4)
    institute_activity = fields.Char(string='Activity in The Institute')
    social_activity = fields.Char(string='Social Activity')

    #language skills
    language_skill = fields.One2many('spc.language.skill', 'ref_id', string='Langauge')

    #special_skills
    thai_typing = fields.Integer(string='Thai word/minute')
    eng_typing = fields.Integer(string='English word/minute')
    computer_program = fields.Boolean(string="Computer Program")
    bike_license_type_id = fields.Many2one('hr.employee.bikelicense', string='Bike License')
    bile_license_number = fields.Char('Driver License No.')
    car_license_type_id = fields.Many2one('hr.employee.carlicense', string='Car License')
    car_license_number = fields.Char('Driver License No.')

    # employment record
    past_job = fields.One2many('hr.employee.pastjob','pastjob_id', string='Record')

    ever_worked_sahagroup = fields.Boolean(string="Have you ever working with SAHA GROUP?")
    work_shift = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Can you work for shift?')
    reason_for_shift = fields.Char('Reason', readonly=True)
    travel = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Can you travelling abroad?')
    reason_travel = fields.Char(string='Reason', readonly=True) 

    # References
    recommend_by = fields.Char('Recommend By')
    recommend_relationship = fields.Char('Relationship')
    recommend_company = fields.Char("Company's Name")    
    recommend_position = fields.Char('Posiion')
    recommend_tel = fields.Integer('Tel.')
    references_line = fields.One2many('hr.employee.ref','ref_id', string='References')


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
