# Hospital Management System (HMS) Module

## Overview
This module manages a **Hospital Management System (HMS)** where users can:  
- Fill patient forms  
- Book appointments  
- Fetch external data (e.g., medicine price and shipment tracking)  
- Track shipments and payments through a payment gateway with status updates  

---

## How to Use

### Patient Model
- Fill out basic patient information.  
- **Validation:** Invalid data triggers warnings or errors via `@api.constrains` or field validation.  
- **Medicine Orders:**  
  - Track medicine shipments with delivery partners.  
  - Fetch current prices based on weight and distance.  
- **Payment:**  
  - Users can be redirected to a dummy payment page.  
  - Payment status updates to **Unpaid**, **Paid**, or **Failed**.  
- **Patient Tags:**  
  - Uses a `Many2many` field linked to `hospital.tags`.  
  - Multiple tags (e.g., diabetic, flu) can be assigned to a patient.  
  - Tags are stored in the database and displayed in the patient form view.  

---

### Doctor Model
- Fill out doctor information:  
  - Name  
  - Age  
  - Specialization  

---

### Appointment Model
- Book appointments linking patients and doctors:  
  - **Patient field:** `Many2one` linked to `hospital.patient`. Patients must exist before booking.  
  - **Doctor field:** `Many2one` linked to `hospital.doctor`. Lists available doctors.  
  - **Notes:** Add specific appointment-related notes.  
  - **Medicine Orders:**  
    - `One2many` field (`appointment_line`) stores multiple medicines per patient.  

---

### View Patient
- **Read-only form view** to display basic patient information.  

---

## Workflow
1. **HMS → Frontdesk → Patient:** Store patient records.  
2. **HMS → Frontdesk → Appointment:** Book and store appointments.  
3. **HMS → Frontdesk → Doctor:** Store doctor records.  
4. **HMS → Frontdesk → View Patient List:** Read-only access to patient information.  
5. **HMS → Configuration → Tags:** Manage and store tag names.  

---

## Notes
- Make sure to create patients before booking appointments.  
- Payment functionality uses a dummy page for testing purposes.  
- Tags can help categorize patients by disease or condition.  
