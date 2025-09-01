from odoo import http
from odoo.http import request

class HospitalPaymentController(http.Controller):

    @http.route('/hospital/payment', type='http', auth='public', website=True, csrf=False)
    def hospital_payment(self, patient_id=None, **kwargs):
        patient = request.env['hospital.patient'].sudo().browse(int(patient_id))
        patient.sudo().write({"payment_status": "paid"})
        return request.render("hospital_management.payment_dummy_template", {
            "patient": patient
        })
