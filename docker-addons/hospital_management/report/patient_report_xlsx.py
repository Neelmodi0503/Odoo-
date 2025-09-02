from odoo import models,fields,api

class PatientReport(models.AbstractModel):
    _name = "report.hospital_management.patient_report_xlsx"
    _description = "Generate Report In XLSX Format"
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self,workbook,data,patients):

        sheet =  workbook.add_worksheet('Patient Report')
        normal = workbook.add_format({'text_wrap': True, 'align' : 'center'})
        bold = workbook.add_format({'bold' : True , 'align' : 'center' })

        sheet.write(0,0,"Name",bold)
        sheet.write(0,1,"Age",bold)
        sheet.write(0,2,"Contact NO ",bold)
        sheet.write(0,3,"Blood Group",bold)
        sheet.write(0,4,"Payment Status",bold)


        row =1
        for patient in patients:
            sheet.write(row, 0, patient.name, normal)
            sheet.write(row, 1, patient.age, normal)
            sheet.write(row ,2, patient.contact_no,normal)
            sheet.write(row, 3, patient.blood_group.name or '', normal)
            sheet.write(row, 4, patient.payment_status or '', normal)
            row += 1
 
