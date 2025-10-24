from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()

def patient_required(view_func):
    return user_passes_test(
        lambda u: hasattr(u, 'patient') or u.is_superuser,
        login_url='patientlogin'
    )(view_func)

def doctor_required(view_func):
    return user_passes_test(
        lambda u: hasattr(u, 'doctor') or u.is_staff,
        login_url='doctorlogin'
    )(view_func)
