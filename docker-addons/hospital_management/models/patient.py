from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
import requests
import logging

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Patient"
    _rec_name = "name"

     #Fields   

    name = fields.Char(string="Patient Name", tracking=True)
    age = fields.Integer(string="Age",compute="compute_age",store=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    email = fields.Char(string="Email",required =True)
    contact_no = fields.Char(string="Contact NO :- ")
    marital_status = fields.Selection(
        [("single", "Single"),
          ("married", "Married")],
            default="single"
    )
    gender = fields.Selection(
        [("male", "Male"),
        ("female", "Female"),
        ("other",'Other')],
        string="Gender",
        default="male",
        tracking=True,
    )

    tag_ids = fields.Many2many(
            "patient.tag", "patient_tag_rel", "patient_id", "tag_id", string="Tags"
        )
    
    _sql_constraints = [
        ('unique_email', 'unique(email)', 'The email must be unique!'),
        ('name_not_null', 'CHECK(name IS NOT NULL)', 'Patient name cannot be empty!'),
    ]

                             #Functions 


    def unlink(self):   
            for rec in self:
                appointments = self.env["hospital.appointment"].search(
                    [("patient_id", "=", rec.id)]
                )
                if appointments:
                    raise ValidationError(  
                        _("Cannot delete patient with existing appointments.")
                    )
            return super(HospitalPatient, self).unlink()

    
    def action_save_and_new(self):
        return {
            "type": "ir.actions.act_window",
            "name": "New Patient",
            "res_model": "hospital.patient",
            "view_mode": "form",
            "target": "current",
            "context": dict(
                self.env.context or {},
                default_name=False,
                default_age=False,  
                default_gender=False,
            ),
        }


    def fetch_external_data(self):
        url = "https://jsonplaceholder.typicode.com/posts" 
        try:
            response = requests.get(url)    
            if response.status_code == 200:
                self.external_data = str(response.json())
                _logger.info("API data fetched successfully")
            else:
                _logger.error("Failed to fetch API data: %s", response.text)
        except Exception as e:
            _logger.error("Error fetching API data: %s", str(e))


    def get_senior_patients(self):
        senior = self.env['hospital.patient'].search([('age', '>', '25')])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Senior Patients',
            'res_model': 'hospital.patient',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', senior.ids)],  
            'target': 'current',
        }
    def add_new_patient(self):
        patient = self.env['hospital.patient'].create({
            'name': 'Hemil Dave',
            'email' : 'hemildave04@gmail.com',
            'contact_no' : "7128867778",
            'date_of_birth' : '2002-03-04', 
    
        })

        _logger.warning("Patient added : %s (ID: %d, Age: %d)", patient.name, patient.id, patient.age)

        return patient

                    #decorators

    @api.constrains("contact_no")
    def check_contact_no_length(self):
        for record in self:
            if record.contact_no:
                if len(record.contact_no) != 10:
                    raise ValidationError("Contact number must be exactly 10 digits")
                if not record.contact_no.isdigit():
                    raise ValidationError("Contact number must contain digits only.")
                if record.email and not record.email.endswith('@gmail.com'):
                    raise ValidationError("Email must be a Gmail address!")



    @api.depends("date_of_birth")
    def compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                rec.age = (
                    today.year
                    - rec.date_of_birth.year
                    - (
                        (today.month, today.day)
                        < (rec.date_of_birth.month, rec.date_of_birth.day)
                    )
                )
            else:
                rec.age = 0

    external_data = fields.Text(string="Enter External Api")





    

