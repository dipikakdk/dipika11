from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from hospital import views
from django.contrib.auth.views import LoginView, LogoutView


#-------------FOR ADMIN RELATED URLS-------------------------------------
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls), #This connects Django’s admin panel
    path('', views.home_view, name='home'), #This defines the home page of your site.
    path('hospital/', include('hospital.urls')),  # Include hospital app URLs

    # Redirects for common typos or nested paths
    path('doctorsignup/doctorlogin/', RedirectView.as_view(url='/doctorlogin/', permanent=False)), #Fix typo when signup + login mixed
    path('doctorlogin/doctorsignup/', RedirectView.as_view(url='/doctorsignup/', permanent=False)), #opposite direction
    path('adminsignup/adminlogin/', RedirectView.as_view(url='/adminlogin/', permanent=False)), #permanent=True means the page has moved forever to a new link
    path('adminlogin/adminsignup/', RedirectView.as_view(url='/adminsignup/', permanent=False)),
    path('patientsignup/patientlogin/', RedirectView.as_view(url='/patientlogin/', permanent=False)),
    path('patientlogin/patientsignup/', RedirectView.as_view(url='/patientsignup/', permanent=False)),

    path('aboutus/', views.aboutus_view, name='aboutus'), #run aboutus_view function form view.py and open aboutus page 
    path('contactus/', views.contactus_view, name='contactus'),


    path('adminclick/', views.adminclick_view), #This page is often for admin login/signup options.
    path('doctorclick/', views.doctorclick_view),
    path('patientclick/', views.patientclick_view),

    path('adminsignup/', views.admin_signup_view, name='adminsignup'), #use admin_signup_view function and show admin sign up
    path('doctorsignup/', views.doctor_signup_view, name='doctorsignup'),
    path('patientsignup/', views.patient_signup_view, name='patientsignup'),
    
    path('adminlogin/', LoginView.as_view(template_name='hospital/adminlogin.html'), name='adminlogin'), #use adminlogin.html template
    path('doctorlogin/', LoginView.as_view(template_name='hospital/doctorlogin.html'), name='doctorlogin'),
    path('patientlogin/', LoginView.as_view(template_name='hospital/patientlogin.html'), name='patientlogin'),


    path('afterlogin/', views.afterlogin_view, name='afterlogin'), #Redirect users after login based on their role
    path('logout/', views.custom_logout, name='logout'),


    path('admin-dashboard/', views.admin_dashboard_view,name='admin-dashboard'), #show admin dashboard (info) after login

    path('admin-doctor/', views.admin_doctor_view,name='admin-doctor'), #show admin doctor page,Page where admin can manage doctors (list, assign, or view)
    path('admin-view-doctor/', views.admin_view_doctor_view,name='admin-view-doctor'), #Admin can see all doctors’ details
    path('delete-doctor-from-hospital/<int:pk>/', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'), #Admin can delete a doctor from the hospital system using their primary key (pk).
    path('update-doctor/<int:pk>/', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor/', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor/', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>/', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>/', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation/',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'), #Admin can view doctors by their specialisation


    path('admin-patient/', views.admin_patient_view,name='admin-patient'), #admin can manage patient(add,update,delete)
    path('admin-view-patient/', views.admin_view_patient_view,name='admin-view-patient'), #Admin can see all patient details
    path('delete-patient-from-hospital/<int:pk>/', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>/', views.update_patient_view,name='update-patient'),
    path('admin-add-patient/', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient/', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>/', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>/', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient/', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>/', views.discharge_patient_view,name='discharge-patient'), #admin can discharge patient
    path('download-pdf/<int:pk>/', views.download_pdf_view,name='download-pdf'), #admin can download patient's discharge summary


    path('admin-appointment/', views.admin_appointment_view,name='admin-appointment'), #Admin page to manage all appointments
    path('admin/profile/', views.admin_profile, name='admin-profile'), #admin profile page
    path('doctor/profile/', views.doctor_profile, name='doctor-profile'), #doctor profile page
    path('patient/profile/', views.patient_profile, name='patient-profile'), #patient profile page 
    path('admin-view-appointment/', views.admin_view_appointment_view,name='admin-view-appointment'), #admin can view all appointments
    path('admin-add-appointment/', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment/', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>/', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>/', views.reject_appointment_view,name='reject-appointment'),
]

#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard/', views.doctor_dashboard_view,name='doctor-dashboard'), #doctor dashboard 

    path('doctor-patient/', views.doctor_patient_view,name='doctor-patient'), #doctor can view his patients 
    path('doctor-view-patient/', views.doctor_view_patient_view,name='doctor-view-patient'), #doctor can view details of a specific patient
    path('doctor-view-discharge-patient/',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),
    path('doctor-appointment/', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment/', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment/',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>/', views.delete_appointment_view,name='delete-appointment'),

    # Queue management URLs
    path('doctor-queue/', views.doctor_queue_view, name='doctor-queue'), #Shows the list of patients in the queue for the doctor
    path('doctor-call-patient/<int:token_id>/', views.doctor_call_patient_view, name='doctor-call-patient'), #calls the next patient in the queue
    path('doctor-complete-consultation/<int:token_id>/', views.doctor_complete_consultation_view, name='doctor-complete-consultation'), #marks the consultation as complete 
]

#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns += [
    path('patient-dashboard/', views.patient_dashboard_view,name='patient-dashboard'), #patient dashboard 
    path('patient-appointment/', views.patient_appointment_view,name='patient-appointment'), #patient can book appointments
    path('patient-book-appointment/', views.patient_book_appointment_view,name='patient-book-appointment'), #Patient can see all their booked appointments
    path('patient-view-appointment/', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient/my_appointments/', views.patient_view_appointment_view,name='my-appointments'),
    path('patient-discharge/', views.patient_discharge_view,name='patient-discharge'), #patient can see their discahrge bills
]

# Serve static files in development, They allow Django to serve static files (CSS, JS) and media files (uploaded images, PDFs) correctly
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

