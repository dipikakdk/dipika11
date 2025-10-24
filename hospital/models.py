from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class Appointment(models.Model):
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctorId = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=500)
    appointmentDate = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False)  # False = pending, True = approved



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)

    def __str__(self):
        return str(self.total)


class QueueToken(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('called', 'Called'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='queue_tokens')
    token_number = models.IntegerField()
    department = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    created_at = models.DateTimeField(default=timezone.now)
    called_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    estimated_wait_time = models.IntegerField(null=True, blank=True, help_text="Estimated wait time in minutes")
    actual_wait_time = models.IntegerField(null=True, blank=True, help_text="Actual wait time in minutes")
    notes = models.TextField(blank=True, null=True)
    called_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='called_tokens')

    class Meta:
        ordering = ['-priority', 'created_at']  # Priority first, then creation time
        indexes = [
            models.Index(fields=['status', 'department']),
            models.Index(fields=['created_at']),
            models.Index(fields=['patient', 'status']),
        ]

    def __str__(self):
        try:
            name = self.patient.user.get_full_name() or self.patient.user.username
        except:
            name = str(self.patient)
        return f"Token {self.token_number} – {name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # Calculate actual wait time when status changes
        if self.status in ['completed', 'cancelled', 'no_show'] and self.called_at and not self.actual_wait_time:
            if self.started_at:
                self.actual_wait_time = int((self.started_at - self.called_at).total_seconds() / 60)
            elif self.completed_at:
                self.actual_wait_time = int((self.completed_at - self.called_at).total_seconds() / 60)

        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """Check if token has been waiting too long"""
        if self.status == 'waiting' and self.created_at:
            wait_time = (timezone.now() - self.created_at).total_seconds() / 60
            return wait_time > 60  # Over 1 hour
        return False

    @property
    def queue_position(self):
        """Get current position in queue"""
        if self.status == 'waiting':
            return QueueToken.objects.filter(
                department=self.department,
                status='waiting',
                created_at__lt=self.created_at
            ).count() + 1
        return None
