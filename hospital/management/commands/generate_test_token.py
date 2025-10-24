from django.core.management.base import BaseCommand
from django.utils import timezone
from hospital.models import Patient, QueueToken

class Command(BaseCommand):
    help = 'Generate a test token for a patient'

    def add_arguments(self, parser):
        parser.add_argument('patient_id', type=int, help='ID of the patient')
        parser.add_argument('--department', type=str, default='Cardiology', help='Department for the token')
        parser.add_argument('--status', type=str, default='waiting', 
                          choices=['waiting', 'called', 'done'],
                          help='Status of the token')

    def handle(self, *args, **kwargs):
        patient_id = kwargs['patient_id']
        department = kwargs['department']
        status = kwargs['status']
        
        try:
            patient = Patient.objects.get(id=patient_id)
            
            # Get the last token number for today
            today = timezone.now().date()
            last_token = QueueToken.objects.filter(
                created_at__date=today
            ).order_by('-token_number').first()
            
            new_token_number = 1
            if last_token:
                new_token_number = last_token.token_number + 1
            
            # Create the token
            token = QueueToken.objects.create(
                patient=patient,
                token_number=new_token_number,
                department=department,
                status=status
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created token #{token.token_number} for {patient.get_name()} ' \n                    f'(Status: {token.get_status_display()}, Department: {token.department})'
                )
            )
            
        except Patient.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'Patient with ID {patient_id} does not exist'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating token: {str(e)}'))
