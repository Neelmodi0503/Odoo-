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
    email = fields.Char(string="Email")
    contact_no = fields.Char(string="Contact NO :- ")
    marital_status = fields.Selection(
        [("single", "Single"), ("married", "Married")], default="single"
    )
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"),("other",'Other')],
        string="Gender",
        default="male",
        tracking=True,
    )
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

    tag_ids = fields.Many2many(
        "patient.tag", "patient_tag_rel", "patient_id", "tag_id", string="Tags"
    )
     #Functions 

    
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
    
         #decorators

    @api.constrains("contact_no")
    def check_contact_no_length(self):
        for record in self:
            if record.contact_no:
                if len(record.contact_no) != 10:
                    raise ValidationError("Contact number must be exactly 10 digits")
                if not record.contact_no.isdigit():
                    raise ValidationError("Contact number must contain digits only.")

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



 



    

