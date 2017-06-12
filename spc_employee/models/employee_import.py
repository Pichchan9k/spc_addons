# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import datetime

import base64
import csv
import sys
import os

class Import(models.Model):
    _name = 'hr.employee.import'

    def import_employee(self):
        arr = []
        csv = base64.decodestring(self.data)
        csv = csv[:csv.index('\n')]
        row = csv[csv.index('\n'):]
        print row
        # employee
        # title_id
        # obj = {
        #     'employee_number': '',
        #     'title_id': '',
        #     'first_name_en': '',
        #     'last_name_en': '',
        #     'first_name_th': '',
        #     'last_name_th': '',
        #     'nick_name_en': '',
        #     'nick_name_th': '',
        #     'departmen_code': '',
        #     'position_code': '',
        #     'signed_date': '',
        #     'onboarding_date': '',
        #     'employee_type': '',
        #     'status': '',
        #     'country_id': '',
        #     'race_id': '',
        #     'citizen_id': '',
        #     'gender': '',
        #     'male': '',
        #     'religion': '',
        #     'marital': '',
        #     'blood_group: ''
        # }

    data = fields.Binary('Import')
