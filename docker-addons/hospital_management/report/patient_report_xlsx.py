from odoo import models,fields,api
from datetime import date

class PatientReport(models.Model):
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
    

class ReportInventory(models.Model):
    _name = "report.hospital_management.inventory_stock_xlsx"
    _description = "Report About Inventory"
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self,workbook,data,quants):
        sheet = workbook.add_worksheet('Inventory')
        bold = workbook.add_format({'bold' : True, 
                                    "align" : 'center',
                                    'valign' : 'vcenter'})

        sheet.write(0,0,"Product Name ",bold)
        sheet.write(0,1,"0-30 days",bold)
        sheet.write(0, 2, '31-60 days ', bold)
        sheet.write(0,3,"60-90 days",bold)
        sheet.write(0,4,"90+ days",bold)


        today = date.today()
        row = 1 
        quants = self.env['stock.quant'].search([("quantity" , '>' , '0')])

        for quant in quants:
            day_0_30 = 0
            day_31_60 = 0 
            day_61_90 = 0 
            day_90_up  = 0

            age = (today - quant.in_date.date()).days

            if age <= 30 :
                day_0_30 = quant.quantity

            elif age <= 60 :
                day_31_60 = quant.quantity
            
            elif age <= 90 :
                day_61_90 = quant.quantity

            else :
                day_90_up = quant.quantity

            sheet.write(row, 0, quant.product_id.display_name)
            sheet.write(row, 1, day_0_30)
            sheet.write(row, 2, day_31_60)
            sheet.write(row, 3, day_61_90)
            sheet.write(row, 4, day_90_up)
            row += 1






    
        
 
