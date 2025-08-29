from odoo import models, fields,api
from datetime import datetime

class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char(string='Tag Name', required=True)


