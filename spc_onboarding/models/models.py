# -*- coding: utf-8 -*-

from odoo import models, fields, api


class onboarding_categoryeq(models.Model):
    _name = 'onboarding.equipment.categoryeq'

    name = fields.Char(string="Category Name", required=True)
    description = fields.Text(string='Description')

class brand(models.Model):
    _name = 'onboarding.equipment.brand'

    name = fields.Char(string='Brand', required=True)

class onboarding_mastereq(models.Model):
    _name = 'onboarding.equipment.mastereq'

    name = fields.Char(string="Equipment Name", required=True)
    category_id = fields.Many2one('maintenance.equipment.category', required=True)
    brand_id = fields.Many2one('onboarding.equipment.brand', required=False)
    description = fields.Text(string='Description')
    responsible_id = fields.Many2one('hr.position', string='Responsible', required=True)
    assign_date = fields.Date(string='Assign Date')
    end_waranty_date = fields.Date(string='End Waranty')
    distributor = fields.Char(string='Distributor')

class Onboarding_equipment(models.Model):
    _name = 'onboarding.equipment'

    name = fields.Char(string='Name', required=True)
    serial_number = fields.Integer(string='Serial')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    for_all = fields.Boolean(string='All')
    equipment_id = fields.Many2many('onboarding.equipment.mastereq', string="Equipment")
    description = fields.Text(string='Description')

    # filter
    department_id = fields.Many2one('hr.department', string='Department')
    position_id = fields.Many2one('hr.position', string='Position')
    # level = fields.Char(string='Level')
    level = fields.Selection([('lv1', '1'), ('lv2', '2'), ('lv3', '3'), ('lv4', '4'), ('lv5', '5'),
                            ('lv6', '6')], string='Level')

    # exclude
    exclude_department_id = fields.Many2one('hr.department', string='Department')
    exclude_position_id = fields.Many2one('hr.position', string='Position')
    exclude_level = fields.Selection([('lv1', '1'), ('lv2', '2'), ('lv3', '3'), ('lv4', '4'), ('lv5', '5'),
                            ('lv6', '6')], string='Level')


class Maintenance_equipment(models.Model):
    _inherit = 'maintenance.equipment'

    owner_user_id = fields.Many2one('hr.employee', string='Owner', track_visibility='onchange')
    responsible_id = fields.Many2one('hr.position', string='Responsible')
    equipment_onboarding_id = fields.Many2many('onboarding.equipment', string='OnBoarding')
    state = fields.Selection([
        ('draft', "Draft"),
        ('process', "Confirmed"),
        ('done', "Done"),
    ], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'

class Employee_equipment(models.Model):
    _inherit = 'hr.employee'

    equipment_onboarding_id = fields.Many2many('maintenance.equipment', string="Equipment")

    def create_equipment(self, employee, equipment):
        equipment = self.env['maintenance.equipment'].sudo().create({
            'name': equipment.name,
            'category_id': equipment.category_id.id,
            'owner_user_id': employee.id
        })
        employee.write({'equipment_onboarding_id': [(4, equipment.id)]})
        return

    # @api.model
    # def create(self, vals):
    #     print 'onboarding create'
    #     employee = super(Employee_equipment, self).create(vals)
    #     for onboarding in self.env['onboarding.equipment'].search([]):
    #         print onboarding
    #         if (onboarding.for_all is True):
    #             print 'f', onboarding.equipment_id
    #             equipment = onboarding.equipment_id
    #             print equipment
    #             print equipment.name, equipment.category_id.id, employee.id
    #             self.create_equipment(employee, onboarding.equipment_id)
    #     return employee