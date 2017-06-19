# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

class OnboardingMastereq(models.Model):
    _name = 'onboarding.equipment.mastereq'

    name = fields.Char(string="Equipment Name", required=True)
    category_id = fields.Many2one('maintenance.equipment.category', required=True)
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    position_id = fields.Many2one('hr.position', string='Position', required=True)
    assign_date = fields.Date(string='Assign Date')
    end_waranty_date = fields.Date(string='End Waranty')
    distributor = fields.Char(string='Distributor')
    description = fields.Text(string='Description')

class OnboardingEquipment(models.Model):
    _name = 'onboarding.equipment'

    name = fields.Char(string='Name', required=True)
    serial_number = fields.Integer(string='Serial')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    for_all = fields.Boolean(string='All')
    equipment_id = fields.Many2many('onboarding.equipment.mastereq', string="Equipment")
    description = fields.Text(string='Description')

    # filter
    department_id = fields.Many2many('hr.department', string='Department')
    position_id = fields.Many2many('hr.position', string='Position')

    # level = fields.Char(string='Level')
    level = fields.Selection([('lv1', '1'), ('lv2', '2'), ('lv3', '3'), ('lv4', '4'), ('lv5', '5'),
                            ('lv6', '6')], string='Level')

    # exclude
    exclude_department_id = fields.Many2many('hr.department', string='Department')
    exclude_position_id = fields.Many2many('hr.position', string='Position')
    exclude_level = fields.Selection([('lv1', '1'), ('lv2', '2'), ('lv3', '3'), ('lv4', '4'), ('lv5', '5'),
                            ('lv6', '6')], string='Level')


class Brand(models.Model):
    _name = 'maintenance.equipment.brand'

    name = fields.Char(string='Brand', required=True)

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.assign_date = datetime.now().strftime("%Y-%m-%d")
        self.state = 'done'

    department_id = fields.Many2one('hr.department_id', string='Department')
    position_id = fields.Many2one('hr.position', string='Position')
    equipment_onboarding_id = fields.Many2many('onboarding.equipment', string='OnBoarding')
    brand_id = fields.Many2one('maintenance.equipment.brand', string='Brand')
    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ], default='draft')

class EmployeeEquipment(models.Model):
    _inherit = 'hr.employee'

    def create_users(self, employee):
        email = ''
        count = 0
        check = False
        while check is False:
            email = '%s.%s%s' % (employee.first_name_en, employee.last_name_en[:count], employee.email)
            user = self.env['res.users'].search([('login', '=', email.lower())])
            if email.lower() == user.login:
                count = count + 1
            else:
                check = True

        res_users = self.env['res.users'].sudo().create({
            'name': employee.name,
            'login': email.lower(),
            'password': '!It3017'
        })
        employee_user = '%s.%s' % (employee.first_name_en, employee.last_name_en[count])
        employee.user = employee_user.lower()
        res_users.partner_id.email = email.lower()
        return res_users

    def equipment_from_onboarding(self, employee):
        print 'equipment_from_onboarding'
        employee = self.env['hr.employee'].search([('id', '=', employee)])
        for onboarding in self.env['onboarding.equipment'].search([]):
            if onboarding.for_all is True:
                for equipment in onboarding.equipment_id:
                    self.create_equipment(employee, equipment, onboarding)

    def create_equipment(self, employee, equipment, onboarding):
        print 'create_equipment'
        equipment = self.env['maintenance.equipment'].sudo().create({
            'name': equipment.name,
            'category_id': equipment.category_id.id,
            'owner_user_id': employee.user_id.id,
            # 'equipment_onboarding_id': onboarding.id,
            # 'master_equipment': master_equipment.id
        })
        employee.write({'equipment_onboarding_id': [(4, equipment.id)]})
        return

    equipment_onboarding_id = fields.Many2many('maintenance.equipment', string="Equipment")
