# Queue Token Generation System - User Guide

## Overview
The Queue Token Generation System is a digital queuing solution that manages patient flow in the hospital. It replaces traditional physical queues with an automated token-based system.

---

## System Components

### 1. **Patient Dashboard (Patient Portal)**
**URL:** `http://127.0.0.1:8000/patient-dashboard/`

#### Features:
- **Get Queue Token Button**: Patients can generate a new queue token with one click
- **Current Token Display**: Shows active token number and status
- **Token Status Indicators**:
  - 🟡 **Waiting**: Yellow badge - Patient is in queue
  - 🔵 **Called**: Blue badge - Patient has been called by doctor
  - ✅ **Done**: Token completed (no longer shown)

#### How Patients Use It:
1. Login to patient account
2. Click on the "Get Token" card on dashboard
3. Token is automatically generated for their assigned doctor's department
4. Token number appears on dashboard (e.g., "Token #5")
5. Wait until status changes from "Waiting" to "Called"
6. When called, proceed to the doctor's office

#### Important Notes:
- Patients can only have **ONE active token per day**
- Token is department-specific (based on assigned doctor)
- Token numbers reset daily
- System prevents duplicate tokens

---

### 2. **Doctor Queue Management (Doctor Portal)**
**URL:** `http://127.0.0.1:8000/doctor-queue/`

#### Features:
- **Real-time Queue Statistics**:
  - Number of patients waiting
  - Currently called patient
  - Total patients in queue

- **Waiting Queue List**:
  - Shows all patients waiting for this department
  - Ordered by arrival time (first come, first served)
  - Displays token number, patient name, and join time

- **Currently in Consultation**:
  - Shows patient currently being attended
  - Option to mark consultation as complete

#### Doctor Actions:
1. **Call Patient**: 
   - Click "Call Patient" button next to waiting patient
   - Status changes from "Waiting" → "Called"
   - Patient receives notification on their dashboard

2. **Mark Complete**:
   - After consultation, click "Mark Complete"
   - Status changes from "Called" → "Done"
   - Patient removed from active queue
   - Next patient can be called

#### Auto-Refresh:
- Page automatically refreshes every 30 seconds
- Ensures real-time queue updates

---

### 3. **Admin Queue Monitor (Admin Portal)**
**URL:** `http://127.0.0.1:8000/admin/hospital/queuetoken/`

#### Features:
- **Statistics Dashboard**:
  - Total waiting tokens
  - Total called tokens
  - Total completed tokens
  - Total tokens today

- **Search & Filters**:
  - Search by patient name or token number
  - Filter by status (waiting/called/done)
  - Filter by department
  - Filter by date

- **Bulk Actions**:
  - Mark multiple tokens as "Waiting"
  - Mark multiple tokens as "Called"
  - Mark multiple tokens as "Done"

- **Table View**:
  - Complete list of all tokens
  - Sortable columns
  - Add/Edit/Delete tokens

---

## Technical Workflow

### Token Generation Process:
1. Patient clicks "Get Token" button
2. System checks if patient already has active token today
3. If no existing token:
   - Retrieves patient's assigned doctor
   - Gets doctor's department
   - Generates next sequential number for that department
   - Creates token with status "waiting"
4. Success message displays token number
5. Token appears on patient dashboard

### Token Lifecycle:
```
[Generated] → Waiting → Called → Done
             (Patient waits) (Doctor calls) (Consultation complete)
```

### Department-Specific Queuing:
- Each department maintains its own queue
- Token numbers are sequential per department
- Example:
  - Cardiology: Token #1, #2, #3...
  - Orthopedics: Token #1, #2, #3...
  - Pediatrics: Token #1, #2, #3...

---

## URL Structure

### Patient URLs:
- Generate Token: `/hospital/generate-token/<patient_id>/`
- Patient Dashboard: `/patient-dashboard/`

### Doctor URLs:
- Queue View: `/doctor-queue/`
- Call Patient: `/doctor-call-patient/<token_id>/`
- Complete Consultation: `/doctor-complete-consultation/<token_id>/`

### Admin URLs:
- Queue Management: `/admin/hospital/queuetoken/`
- Add Token: `/admin/hospital/queuetoken/add/`

---

## Database Structure

### QueueToken Model Fields:
- `token_number`: Sequential number for the day
- `patient`: Foreign key to Patient
- `department`: Department name (from assigned doctor)
- `status`: waiting | called | done
- `created_at`: Timestamp when token was created
- `called_at`: Timestamp when patient was called (nullable)
- `completed_at`: Timestamp when consultation ended (nullable)

---

## Features & Benefits

✅ **Automated**: No manual token management required  
✅ **Fair**: First-come, first-served based on creation time  
✅ **Department-specific**: Separate queues per department  
✅ **Real-time**: Live updates for patients and doctors  
✅ **Duplicate Prevention**: One token per patient per day  
✅ **Admin Control**: Full oversight and management capabilities  
✅ **Mobile-friendly**: Accessible from any device  
✅ **Auto-refresh**: No need to manually refresh pages  

---

## Testing the System

### As a Patient:
1. Login with patient credentials
2. Go to dashboard
3. Click "Get Token" card
4. Verify token appears with "Waiting" status
5. Wait for doctor to call

### As a Doctor:
1. Login with doctor credentials
2. Click "Patient Queue" in sidebar
3. View waiting patients
4. Click "Call Patient" for first in queue
5. After consultation, click "Mark Complete"

### As an Admin:
1. Login to admin portal
2. Navigate to Queue tokens
3. View statistics and manage tokens
4. Use bulk actions to update multiple tokens
5. Generate reports

---

## Common Issues & Solutions

### Issue: Can't generate token
- **Solution**: Check if patient already has an active token today
- Verify patient has an assigned doctor

### Issue: Token not appearing
- **Solution**: Refresh the page or check if token was created in admin

### Issue: Queue not updating
- **Solution**: Wait 30 seconds for auto-refresh or manually refresh

### Issue: Wrong department
- **Solution**: Verify patient's assigned doctor's department in admin

---

## Future Enhancements
- SMS/Email notifications when token is called
- Estimated wait time calculations
- Queue analytics and reporting
- Multi-doctor department handling
- Token cancellation by patient
- Priority tokens for emergencies

---

## Support
For technical issues or feature requests, contact the system administrator.
