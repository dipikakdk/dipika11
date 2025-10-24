# Queue and Token System for Hospital Management System

This document provides an overview of the Queue and Token System implemented in the Hospital Management System.

## Features

1. **Token Generation**: Generate tokens for patients with automatic numbering
2. **Queue Management**: View and manage the queue of patients
3. **Status Tracking**: Track token status (Waiting, Called, Done)
4. **Department-wise Queues**: Support for different departments
5. **Real-time Updates**: Auto-refreshing interface for real-time updates

## Setup

1. **Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Admin Interface**:
   - The QueueToken model is registered in the admin interface
   - Access it at `/admin/hospital/queuetoken/`

## Usage

### For Doctors/Admins

1. **View Queue**:
   - Navigate to `/hospital/queue/` to view the current queue
   - The queue is divided into three sections: Waiting, In Consultation, and Completed

2. **Generate Token**:
   - Go to a patient's profile
   - Click the "Generate Token" button (visible to doctors/admins only)
   - The system will automatically assign the next available token number

3. **Update Token Status**:
   - **Call Next Patient**: Click "Call" next to a waiting patient to move them to "In Consultation"
   - **Mark as Done**: Click "Done" when the consultation is complete

4. **View Current Token**:
   - Navigate to `/hospital/current-token/` to see the currently serving patient
   - This page auto-refreshes every 30 seconds

### For Testing

You can generate test tokens using the management command:

```bash
# Generate a test token for patient with ID 1
python manage.py generate_test_token 1 --department "Cardiology" --status "waiting"
```

## API Endpoints

- `GET /hospital/queue/` - View the queue
- `POST /hospital/generate-token/<patient_id>/` - Generate a new token for a patient
- `GET /hospital/update-token/<token_id>/<status>/` - Update token status
- `GET /hospital/current-token/` - View the current token being served

## Security

- Only authenticated users can access the queue system
- Only doctors and admins can generate tokens and update their status
- Patients can only view their own tokens

## Troubleshooting

- **Token not appearing in queue**: Ensure the token's status is set to 'waiting'
- **Permission denied**: Make sure you're logged in as a doctor or admin
- **Page not refreshing**: Check your browser's JavaScript console for errors

## Future Enhancements

1. Sound notifications for new tokens
2. Multiple queue support for different departments
3. Estimated wait times for patients
4. SMS/Email notifications for patients
5. Priority queue for emergency cases
