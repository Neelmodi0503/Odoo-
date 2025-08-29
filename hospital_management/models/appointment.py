from odoo import models, fields, api

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'
    _rec_name_search = ['patient_id','reference']


    reference = fields.Char(string='Reference', readonly=True, copy=False, default='New')
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=False)
    date_of_appointment = fields.Date(string="Date of Appointment", required=True)
    doctor_id = fields.Many2one('hospital.doctor',string='Available Doctors')
    note = fields.Text(string='Notes')
    state = fields.Selection([  
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('ongoing','Ongoing'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')     
    ], string='Status', default='draft', required=True,tracking=True)
    appointment_line_ids = fields.One2many('hospital.appointment.line','appointment_id', string ='Description')

    @api.onchange('date_of_appointment')
    def check_date(self):
            if self.date_of_appointment and self.date_of_appointment < fields.Date.today():
                return {
                    "warning" :{
                        'title' : "invalid date",
                        'message' : "you can not select past date for appointment"
                    
                    }
                }
        

    @api.model_create_multi
    def create(self,vals_list):
        print("Appointments Lists",vals_list)
        for vals in vals_list:
            if not  vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)  

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_ongoing(self):
        for rec in self:
            rec.state = 'ongoing'
    
    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'hospital appointment line'

    appointment_id = fields.Many2one('hospital.appointment',string = 'Appointment Line')
    product_id = fields.Many2one('product.product', string='product')
    qty = fields.Float(string="Quantity")