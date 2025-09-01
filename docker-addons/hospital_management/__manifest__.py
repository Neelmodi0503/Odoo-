{
    "name": "Hospital Management",
    "version": "1.0",
    "author": "Neel Modi",
    "depends": ["base", "mail", "product","sale",'crm','website'],
    "license":'LGPL-3',
    'sequence':"1",
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "report/reports.xml",
        "views/patient_view.xml",
        "views/appointment_view.xml",
        "views/appointment_line_view.xml",
        "views/readonly.xml",
        "views/patient_tag_view.xml",
        'views/crm_lead_wizard.xml',
        'views/crm_lead_confirm_wizard_action.xml',
        'views/crm_lead_inherit_view.xml',
        'views/wizard.xml',
        'views/doctor_view.xml',
        "views/menu.xml"
    ],
    "application": True,         
    "installable": True 
}
