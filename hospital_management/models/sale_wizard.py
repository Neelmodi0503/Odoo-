from odoo import models , fields

class CrmLeadConfirmWizard(models.TransientModel):
    _name = "crm.lead.confirm.wizard"
    _description = 'Crm Leads Wizard'

    confirm_message = fields.Char(string= 
            "Message",
             default="Are you sure you want to convert this lead into an opportunity?",
             readonly=True
            )
    def action_confirm_conversion(self):
        active_id = self.env.context.get('active_id')
        lead = self.env["crm.lead"].browse(active_id)
        if lead:
            lead.type = 'opportunity'
        return {"type" : 'ir.actions.act_window_close'}
    
