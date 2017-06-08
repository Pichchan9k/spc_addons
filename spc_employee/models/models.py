# -*- coding: utf-8 -*-
from odoo import models, fields, api ,exceptions
from datetime import datetime

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

class EducationLevel:
    def get_education_level(self):
        print 'get_education_level'
        return [('primery', 'Primary School'), ('secondary', 'Secondary School'), ('high', 'High School'), ('college/vocational', 'College'), ('bachelor', 'Bachelor Degree'), ('higher', 'Master Degree or higher')]

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

class LangageSkillName(models.Model):
    _name = 'spc.language.skill.name'

    name = fields.Char('Lanugage Name', required=True)

class LanguageSkill(models.Model):
    _name = 'spc.language.skill'

    def get_language_skill(self):
        return [('fair', 'Fair'), ('good', 'Good'), ('excellent', 'Excellent')]

    name = fields.Many2one('spc.language.skill.name', string='Language', required=True)
    speak_skill = fields.Selection(get_language_skill, string='Speak', required=True)
    read_skill = fields.Selection(get_language_skill, string='Read', required=True)
    write_skill = fields.Selection(get_language_skill, string='Write', required=True)
    languageskill_id = fields.Many2one('hr.employee', string='LanguageSkil Reference', index=True, required=False, ondelete='cascade')

class Institue(models.Model):
    _name = 'spc.institute'

    name = fields.Char(string='Institute', required=True)

class Education(models.Model):
    _name = 'spc.employee.edu'

    name = fields.Selection(EducationLevel().get_education_level(), string='Education Level', required=True)
    institute = fields.Many2one('spc.institute', string='Instutue', required=True)
    institute_type = fields.Selection([('domestic', 'Domestic'), ('abroad', 'Abroad')], string='Institute Type', required=True)
    major = fields.Char(string='Major', required=True)
    gpa = fields.Float(string='G.P.A.', required=True)
    start_study = fields.Date(string='From', required=True)
    end_study = fields.Date(string='To', required=True)
    education_id = fields.Many2one('hr.employee', string='Education Reference', index=True, required=False, ondelete='cascade')

class TrainingCourse(models.Model):
    _name = 'spc.training.course'

    name = fields.Char('Items', required=True)
    institute = fields.Char('Institute', required=True)
    period = fields.Integer('Period', required=True)
    date = fields.Date('Day Month Year', required=True)
    training_id = fields.Many2one('hr.employee', string='Training Ref', index=True, required=False, ondelete='cascade')

class Religion(models.Model):
    _name = 'hr.employee.religion'

    @api.multi
    def name_get(self):
        return NameGet().name_get(self)

    name = fields.Char('Religion EN')
    name_th = fields.Char('Religion TH')


class NameTitle(models.Model):
    _name = 'hr.employee.title'

    # @api.multi
    # def name_get(self):
    #     return NameGet().name_get(self)

    name = fields.Char('Title')
    name_th = fields.Char('Title Th')

class PastJob(models.Model):
    _name = 'hr.employee.pastjob'
    _order = 'start_date'

    name = fields.Char(string='Company', required=True)
    company_address = fields.Char(string='Address', required=True)
    company_type = fields.Selection([('sahagroup', 'Saha Group'), ('present', 'Present'), ('past', 'Past')], string='Type')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    first_position = fields.Char(string='First Position', required=True)
    last_poition = fields.Char(string='Last Position', required=True)
    start_salary = fields.Integer(string='Starting Salary', required=True)
    final_salary = fields.Integer(string='Final Salary', required=True)
    reason_for_leave = fields.Char(string='Reason For Changing', required=True)
    pastjob_id = fields.Many2one('hr.employee', string='Pastjob Reference', index=True)

class CarLicense(models.Model):
    _name = 'hr.employee.bikelicense'

    name = fields.Char(string='Type')

class BikeLicense(models.Model):
    _name = 'hr.employee.carlicense'

    name = fields.Char(string='Type')

class References(models.Model):
    _name = 'hr.employee.ref'

    name = fields.Char(string='Name')
    company = fields.Char(string='Company')
    relationship = fields.Char(string='Relatonship')
    ref_type = fields.Selection([('ref', 'References'), ('saha_group', 'Saha Group'), ('not_family', 'Not is family')], string='Type')
    postion = fields.Char(string='Position')
    tel = fields.Char(string='Tel')
    ref_id = fields.Many2one('hr.employee', string='Persons Reference', index=True)

class Children(models.Model):
    _name = 'hr.employee.children'

    def child_age(self):
        now_year = datetime.now().strftime("%Y")
        for record in self:
            year_of_birthday = record.birth_date[:4]
            record.age = int(now_year) - int(year_of_birthday)

    name = fields.Char('Name', required=True)
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Sex', required=True)
    birth_date = fields.Date(string='Date of Birth', required=True)
    age = fields.Char('Age', compute=child_age)
    education_level = fields.Selection(EducationLevel().get_education_level(), string='Education Level', required=True)
    children_id = fields.Many2one('hr.employee', string='Children Ref', index=True, required=False, ondelete='cascade')

class TelephoneType(models.Model):
    _name = 'spc.telephone.type'

    name = fields.Char('Type', required=True)
    name_th = fields.Char('Type', required=True)

class Telephone(models.Model):
    _name = 'spc.telephone'

    name = fields.Char('Number', required=True)
    tel_type = fields.Many2one('spc.telephone.type', string='Type', required=True)
    tel_id = fields.Many2one('hr.employee', string='Telephone Ref', index=True, required=False, ondelete='cascade')

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

    @api.constrains('citizen_id')
    def constrains_cid(self):
        print 'citizen_id'
        cid = self.citizen_id
        if (cid is not False):
            if(len(cid) != 13):
                print("false")
                raise exceptions.ValidationError("Please Input CitizenID 13 number")

            for char in cid:
                if char.isdigit() is False:
                    print("false")
                    raise exceptions.ValidationError("Please Input only number")
            num = 0
            num2 = 13
            ciddata = list(cid)
            sum = 0
            while num < 12:
                sum += int(ciddata[num]) * (num2 - num)
                num += 1
            digit13 = sum % 11
            if digit13 == 0:
                digit13 = 1
            elif digit13 == 1:
                digit13 = 0
            else:
                digit13 = 11 - digit13
            # if digit13 == int(ciddata[12]):
                # return True
            if digit13 != int(ciddata[12]):
               raise exceptions.ValidationError("Please Input real citizen number")


    @api.onchange('first_name_en', 'last_name_en')
    def name_en(self):
        self.name = '%s %s' % (self.first_name_en, self.last_name_en)
        if self.first_name_en is not False and self.last_name_en is not False:
            email = '%s.%s' % (self.first_name_en, self.last_name_en[0][:1])
            self.user = email.lower()

    @api.onchange('first_name_th', 'last_name_th')
    def name_th(self):
        self.name_th = '%s %s' % (self.first_name_th, self.last_name_th)

    def employee_age(self):
        now_year = datetime.now().strftime("%Y")
        for record in self:
            year_of_birthday = record.birthday[:4]
            record.age = int(now_year) - int(year_of_birthday)

    def employee_duration(self):
        print 'employee duration'
        now_year = datetime.now().strftime("%Y")
        now_month = datetime.now().strftime("%m")
        for record in self:
            year_of_start = record.start_date[:4]
            year_of_dulation = int(now_year) - int(year_of_start)

            month_of_start = record.start_date[5:][:2]
            mounth_of_duration = int(now_month) - int(month_of_start)

            record.duration_of_employment = '%s/%02d' % (year_of_dulation, mounth_of_duration)
            print record.duration_of_employment
    name_th = fields.Char('Name Thai')
    user = fields.Char('Username', readonly=False, required=True)
    email = fields.Selection([('@sahapatco.th', '@sahapat.co.th'), ('@sahapat.com', '@sahapat.com')], default='@sahapatco.th', string='Email', required=True)
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
    blood_group = fields.Selection([('a', 'A'), ('b', 'B'), ('ab', 'AB'), ('o', 'O')], string='Blood Group')
    religion = fields.Many2one('hr.employee.religion', string='Religion')
    citizen_id = fields.Char('CitizenID', size=13)
    onboarding_date = fields.Date('Onboarding Date', required=True)
    sign_contact_date = fields.Date('Signed Date', required=True)
    start_date = fields.Date('Start Date', required=True)
    probation_end_date = fields.Date('ProbationEnd Date')
    start_date = fields.Date('Start Date')
    employee_number = fields.Char(string='Employee ID')
    social_line = fields.Char('Line Id')
    social_facebook = fields.Char('Facebook')
    personal_disease = fields.Char('Personal Disease')
    allergy = fields.Char('Allergy')
    race_id = fields.Many2one('res.country', string='Race')
    age = fields.Integer('Age', compute=employee_age)
    duration_of_employment = fields.Char('Duration of Employee', compute=employee_duration)
# ]fdgdfsgds
    #telephone
    tel_line = fields.One2many('spc.telephone', 'tel_id', string='Telephone', copy=True)

    #address
    address_line = fields.One2many('spc.address', 'address_id', string='Address', copy=True)

    #children
    children_line = fields.One2many('hr.employee.children', 'children_id', string='No. of Children', copy=True)
    # education background
    education = fields.One2many('spc.employee.edu', 'education_id', string='Education Background')
    intend_further_study = fields.Selection([('no', 'No'), ('yes', 'Yes'), ('domestic', 'Domestic'), ('abroad', 'Abroad')], string='Intend to further study')
    studying_at = fields.Many2one('spc.institute', string='Studying at')
    studying_major = fields.Char(string='Major')
    studying_year_of_end = fields.Char(string='Year of graduation', limit=4)
    institute_activity = fields.Char(string='Activity in The Institute')
    social_activity = fields.Char(string='Social Activity')

    #training course
    training_line = fields.One2many('spc.training.course', 'training_id', string='Training Course')

    #language skills
    language_skill = fields.One2many('spc.language.skill', 'languageskill_id', string='Langauge')

    #special_skills
    thai_typing = fields.Integer(string='Thai word/minute')
    eng_typing = fields.Integer(string='English word/minute')
    computer_program = fields.Boolean(string="Computer Program")
    bike_license_type_id = fields.Many2one('hr.employee.bikelicense', string='Bike License')
    bile_license_number = fields.Char('Driver License No.')
    car_license_type_id = fields.Many2one('hr.employee.carlicense', string='Car License')
    car_license_number = fields.Char('Driver License No.')

    # employment record
    past_job = fields.One2many('hr.employee.pastjob', 'pastjob_id', string='Record')

    ever_worked_sahagroup = fields.Boolean(string="Have you ever working with SAHA GROUP?")
    work_shift = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Can you work for shift?', required=True)
    reason_for_shift = fields.Char('Reason')
    travel = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Can you travelling abroad?', required=True)
    reason_travel = fields.Char(string='Reason')
    work_shift = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Can you work for shift?')
    reason_for_shift = fields.Char('Reason', readonly=True)
    travel = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Can you travelling abroad?')
    reason_travel = fields.Char(string='Reason', readonly=True)

    # References
    references_line = fields.One2many('hr.employee.ref', 'ref_id', string='References')

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
    # dsfsa

    # create send to ad > 4 param id, firstname lastname domain
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
