from odoo import models , fields,api,_
from  datetime import date
import logging
import pdb
import datetime
_logger = logging.getLogger(__name__)

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = "Hospital Doctors"
    _rec_name = 'name'

    name = fields.Char(string= "Name :- " )
    age = fields.Integer(string = "Age :- " , compute="compute_age",store=True)
    specialist = fields.Char(string= "Specialization")
    date_of_birth = fields.Date(string = 'Date of Birth ')
    gender = fields.Selection(
        [("male", "Male"),
        ("female", "Female"),
        ("other",'Other')],
        string="Gender",
        default="male",
    ) 
    @api.depends('date_of_birth')
    def compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = (
                    today.year
                    - rec.date_of_birth.year
                    - ((today.month, today.day) < (rec  .date_of_birth.month, rec.date_of_birth.day))
                )
            else:
                rec.age = 0

    def cron_test_doctor(self):
        _logger.warning(">>> CRON JOB RUNNING SUCCESSFULLY <<<")
        doctors = self.search([])
        for doc in doctors:
            _logger.info("Doctor Found: %s (Age: %s)", doc.name, doc.age)









