from odoo import models, fields, api

class HospitalWizard(models.TransientModel):
    _name = 'hospital.wizard'
    _description = "Hospital Wizard"

    followup_date = fields.Date(string="Follow-up Date")
    note = fields.Text(string="Note")

    def action_apply(self):
        active_ids = self.env.context.get('active_ids')
        patients = self.env["hospital.patient"].browse(active_ids)

        for patient in patients:
            patient.message_post(
                body=f"<b>Follow-up Date:</b> {self.followup_date or 'N/A'}<br/>"
                     f"<b>Note:</b> {self.note or ''}"
            )
