from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Doctor, Patient, Appointment, PatientDischargeDetails, QueueToken

# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'department', 'mobile', 'status_badge')
    list_filter = ('department', 'status')
    search_fields = ('user__first_name', 'user__last_name', 'mobile')

    def status_badge(self, obj):
        if obj.status:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 12px;">Active</span>')
        else:
            return format_html('<span style="background-color: #ffc107; color: black; padding: 3px 8px; border-radius: 12px; font-size: 12px;">Pending</span>')
    status_badge.short_description = 'Status'

class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'mobile', 'symptoms', 'status_badge', 'get_assigned_doctor')
    list_filter = ('status', 'assignedDoctorId')
    search_fields = ('user__first_name', 'user__last_name', 'mobile', 'symptoms')

    def status_badge(self, obj):
        if obj.status:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 12px;">Admitted</span>')
        else:
            return format_html('<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 12px; font-size: 12px;">On Hold</span>')
    status_badge.short_description = 'Status'

    def get_assigned_doctor(self, obj):
        if obj.assignedDoctorId:
            try:
                doctor = Doctor.objects.get(user_id=obj.assignedDoctorId)
                return format_html('<a href="{}" style="color: #007bff;">{}</a>',
                                 reverse('admin:hospital_doctor_change', args=[doctor.id]),
                                 doctor.get_name)
            except Doctor.DoesNotExist:
                return "Not Assigned"
        return "Not Assigned"
    get_assigned_doctor.short_description = 'Assigned Doctor'

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'appointmentDate', 'description', 'status_badge')
    list_filter = ('status', 'appointmentDate')
    search_fields = ('patientId__user__first_name', 'patientId__user__last_name', 'doctorId__user__first_name', 'doctorId__user__last_name', 'description')

    def get_patient_name(self, obj):
        return obj.patientId.get_name if obj.patientId else "No Patient"
    get_patient_name.short_description = 'Patient'
    get_patient_name.admin_order_field = 'patientId'

    def get_doctor_name(self, obj):
        return obj.doctorId.get_name if obj.doctorId else "No Doctor"
    get_doctor_name.short_description = 'Doctor'
    get_doctor_name.admin_order_field = 'doctorId'

    def status_badge(self, obj):
        if obj.status:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 12px;">Approved</span>')
        else:
            return format_html('<span style="background-color: #ffc107; color: black; padding: 3px 8px; border-radius: 12px; font-size: 12px;">Pending</span>')
    status_badge.short_description = 'Status'

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    list_display = ('patientName', 'assignedDoctorName', 'releaseDate', 'total_amount')
    list_filter = ('releaseDate',)
    search_fields = ('patientName', 'assignedDoctorName')

    def total_amount(self, obj):
        return f"₹{obj.total:,}"
    total_amount.short_description = 'Total Amount'

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)


@admin.register(QueueToken)
class QueueTokenAdmin(admin.ModelAdmin):
    list_display = ('token_number', 'patient_info', 'department', 'status', 'priority', 'created_at', 'called_at')
    list_filter = ('status', 'department', 'priority', 'created_at')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'token_number')
    ordering = ('-created_at',)
    list_per_page = 20
    actions = ['mark_waiting', 'mark_called', 'mark_done']

    # Add readonly fields for timestamps
    readonly_fields = ('created_at', 'called_at', 'started_at', 'completed_at')

    # Custom field configuration
    def get_list_filter(self, request):
        return ('status', 'department', 'priority', 'created_at')

    def get_search_fields(self, request):
        return ('patient__user__first_name', 'patient__user__last_name', 'token_number')

    def patient_info(self, obj):
        try:
            if obj.patient:
                return str(obj.patient)
            return 'No Patient'
        except:
            return 'Error'
    patient_info.short_description = 'Patient'
    patient_info.admin_order_field = 'patient'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Add statistics for the template
        from django.utils import timezone
        today = timezone.now().date()

        extra_context['waiting_count'] = QueueToken.objects.filter(status='waiting', created_at__date=today).count()
        extra_context['called_count'] = QueueToken.objects.filter(status='called', created_at__date=today).count()
        extra_context['done_count'] = QueueToken.objects.filter(status='completed', created_at__date=today).count()
        extra_context['total_count'] = QueueToken.objects.filter(created_at__date=today).count()

        return super().changelist_view(request, extra_context=extra_context)

    def mark_waiting(self, request, queryset):
        updated = queryset.update(status='waiting')
        self.message_user(request, f"Marked {updated} tokens as waiting.")
    mark_waiting.short_description = "Mark selected as Waiting"

    def mark_called(self, request, queryset):
        updated = queryset.update(status='called')
        self.message_user(request, f"Marked {updated} tokens as called.")
    mark_called.short_description = "Mark selected as Called"

    def mark_done(self, request, queryset):
        updated = queryset.update(status='completed')  # Changed to match model
        self.message_user(request, f"Marked {updated} tokens as completed.")
    mark_done.short_description = "Mark selected as Completed"
