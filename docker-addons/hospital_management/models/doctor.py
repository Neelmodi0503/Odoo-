from odoo import models , fields,api
from  datetime import date

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
        tracking=True,
    )   
    @api.depends('date_of_birth')
    def compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = (
                    today.year
                    - rec.date_of_birth.year
                    - ((today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
                )
            else:
                rec.age = 0




