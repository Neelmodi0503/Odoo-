from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
import logging
import requests


_logger = logging.getLogger(__name__)

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Patient"
    _rec_name = "name"
    

    name = fields.Char(string="Patient Name", tracking=True)
    age = fields.Integer(string="Age",compute="compute_age",inverse="_set_age",store=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    email = fields.Char(string="Email",required =True)
    contact_no = fields.Char(string="Contact NO :- ")
    image = fields.Image(string="Profile Image")
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
    )
    price = fields.Float(string= "price")
    tracking_number = fields.Char(string="tracking_number")
    status= fields.Char(string="status")
    shipping_price = fields.Float(string="Shipping Price")
    shipping_status = fields.Char(string="Shipping Status")
    payment_status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ], default='unpaid',
        readonly=True)
    external_data = fields.Text(string="Enter External Api")

    tag_ids = fields.Many2many(
            "patient.tag", "patient_tag_rel", "patient_id", "tag_id", string="Tags"
        )   
   

                             #Functions 


    """ This Function Will restrict patient record 
        being deleted if its appoitment exists """


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
    

    """ This Function will save the record
         with button and than clear form fields  """
    
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
    
    """ This Function Will fetch The shipping Price and tha update it in the ui"""


    def action_shipping(self):
        response = {
            "price": 150.0,
            "tracking_number": "DUMMY123456",
            "status": "shipped"
        }
        self.write({
            "shipping_price": response["price"],
            "tracking_number": response["tracking_number"],
            "shipping_status": response["status"]
        })
        return True
    
    def action_update_tracking(self):
        """Dummy API call for tracking status update"""
        response = {
            "tracking_number": self.tracking_number,
            "status": "delivered"
        }
        self.write({
            "shipping_status": response["status"]
        })
        return True
    
    """ This Will redirect user to dummy page and than update the payment status """

    def action_pay_now(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return {
            "type": "ir.actions.act_url",
            "target": "self",
            "url": f"{base_url}/hospital/payment?patient_id={self.id}"
    }

    """ This will fetch external  url and show data accordingly """


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

    """ This will show senior patient list """


    def get_senior_patients(self):
        senior = self.env['hospital.patient'].search([('age', '>', '25')])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Senior Patients',
            'res_model': 'hospital.patient',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', senior.ids)],  
            'target': 'current'
        }
    
    """This will used to add new patient """


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

    """ This is used for validating email """


    @api.constrains("email")
    def check_contact_no_length(self):
        for record in self:
            if record.email and not record.email.endswith('@gmail.com'):
                 raise ValidationError("Email must be a Gmail address!")
        
    """ used to  check length of contact number """
    
    @api.onchange('contact_no')
    def check_digit(self):
        for rec in self:
            if rec.contact_no and rec.contact_no != 10 :
                raise ValidationError ("Contact Number Must be 10 Digits ")
            
    """ Raise a warning if name is only digit """
    
    @api.onchange('name')
    def check_name(self):
        for rec in self:
            if rec.name and  rec.name.isdigit():
               return {
                   'warning':{
                       'title' :'invalid name',
                       'message' : 'name must be characters'
                   }
                   
               }
    """ Data base level Validation """
        

    _sql_constraints = [
        ('unique_email', 'unique(email)', 'The email must be unique!'),
        ('name_not_null', 'CHECK(name IS NOT NULL)', 'Patient name cannot be empty!'),
    ]
    """ Used to compute age based on  dob"""
                
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

    def _set_age(self):
        today = date.today()
        for rec in self:
            if rec.age:
                rec.date_of_birth = date(today.year - rec.age, today.month, today.day)



                
                
            
    









    

