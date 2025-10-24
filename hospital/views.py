from django.shortcuts import render, redirect, reverse, get_object_or_404
from . import forms, models
from django.db.models import Sum, Max
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout
from datetime import datetime, timedelta, date
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone

#-----------for checking user is doctor , patient or admin 
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


# Queue System Views
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def generate_token(request, patient_id):
    # Allow patients to generate tokens for themselves, or staff/doctors to generate for any patient
    if request.user.groups.filter(name='PATIENT').exists():
        # If user is a patient, they can only generate tokens for themselves
        patient = get_object_or_404(models.Patient, user=request.user)
        if str(patient.id) != str(patient_id):
            return HttpResponse('Unauthorized', status=403)
    elif not (request.user.is_staff or request.user.groups.filter(name='DOCTOR').exists()):
        return HttpResponse('Unauthorized', status=401)
    else:
        patient = get_object_or_404(models.Patient, id=patient_id)
    
    today = timezone.now().date()
    last_token = models.QueueToken.objects.filter(created_at__date=today).aggregate(Max('token_number'))['token_number__max']
    new_num = 1 if last_token is None else last_token + 1

    # Prevent duplicate waiting token for same patient
    exists = models.QueueToken.objects.filter(
        patient=patient, 
        created_at__date=today, 
        status='waiting'
    ).exists()
    
    if exists:
        messages.info(request, "You already have a waiting token.")
        return redirect('patient-dashboard')

    # Get department from patient's assigned doctor or use default
    department = ''
    if patient.assignedDoctorId:
        try:
            doctor = models.Doctor.objects.get(id=patient.assignedDoctorId)
            department = doctor.department
        except models.Doctor.DoesNotExist:
            pass

    token = models.QueueToken.objects.create(
        patient=patient, 
        token_number=new_num, 
        department=department,
        status='waiting'
    )
    
    messages.success(request, f"Token #{new_num} generated successfully!")
    return redirect('patient-dashboard')
    # Allow patients to generate tokens for themselves, or staff/doctors to generate for any patient
    if request.user.groups.filter(name='PATIENT').exists():
        # If user is a patient, they can only generate tokens for themselves
        patient = get_object_or_404(models.Patient, user=request.user)
        if str(patient.id) != str(patient_id):
            return HttpResponse('Unauthorized', status=403)
    elif not (request.user.is_staff or request.user.groups.filter(name='DOCTOR').exists()):
        return HttpResponse('Unauthorized', status=401)
    else:
        patient = get_object_or_404(models.Patient, id=patient_id)
    
    today = timezone.now().date()
    last_token = models.QueueToken.objects.filter(created_at__date=today).aggregate(Max('token_number'))['token_number__max']
    new_num = 1 if last_token is None else last_token + 1

    # Prevent duplicate waiting token for same patient
    exists = models.QueueToken.objects.filter(
        patient=patient, 
        created_at__date=today, 
        status='waiting'
    ).exists()
    
    if exists:
        messages.info(request, "You already have a waiting token.")
        return redirect('patient-dashboard')

    # Get department from patient's assigned doctor or use default
    department = ''
    if patient.assignedDoctorId:
        try:
            doctor = models.Doctor.objects.get(id=patient.assignedDoctorId)
            department = doctor.department
        except models.Doctor.DoesNotExist:
            pass

    token = models.QueueToken.objects.create(
        patient=patient, 
        token_number=new_num, 
        department=department,
        status='waiting'
    )
    
    messages.success(request, f"Token #{new_num} generated successfully!")
    return redirect('patient-dashboard')


@login_required
def queue_list(request):
    if not request.user.is_authenticated or not (request.user.is_staff or request.user.groups.filter(name='DOCTOR').exists()):
        return HttpResponse('Unauthorized', status=401)
        
    today = timezone.now().date()
    tokens_waiting = models.QueueToken.objects.filter(
        created_at__date=today, 
        status='waiting'
    ).order_by('token_number')
    
    tokens_called = models.QueueToken.objects.filter(
        created_at__date=today, 
        status='called'
    ).order_by('created_at')
    
    tokens_done = models.QueueToken.objects.filter(
        created_at__date=today, 
        status='done'
    ).order_by('-created_at')

    return render(request, 'hospital/queue_list.html', {
        'tokens_waiting': tokens_waiting,
        'tokens_called': tokens_called,
        'tokens_done': tokens_done,
    })


@login_required
def update_token_status(request, token_id, new_status):
    if not request.user.is_authenticated or not (request.user.is_staff or request.user.groups.filter(name='DOCTOR').exists()):
        return HttpResponse('Unauthorized', status=401)
        
    token = get_object_or_404(models.QueueToken, id=token_id)
    if new_status not in ('waiting', 'called', 'done'):
        messages.error(request, "Invalid status")
    else:
        token.status = new_status
        token.save()
        messages.success(request, f"Token {token.token_number} has been marked as {new_status}.")
    return redirect('queue_list')


@login_required
def current_token_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
        
    today = timezone.now().date()
    current_token = models.QueueToken.objects.filter(
        created_at__date=today, 
        status='called'
    ).order_by('created_at').last()  # Get the most recently called token
    
    return render(request, 'hospital/current_token.html', {'current': current_token})


# Regular views

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')


#for showing signup/login button for admin 
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


#for showing signup/login button for doctor 
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for showing signup/login button for patient 
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')




def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})




def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'hospital/patientsignup.html',context=mydict)






# Custom logout view that handles both GET and POST requests
def custom_logout(request):
    auth_logout(request)
    return redirect('home')

#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('home')

        # Check if user is admin (including superuser and staff)
        if request.user.is_superuser or request.user.is_staff or is_admin(request.user):
            return redirect('admin-dashboard')
        elif is_doctor(request.user):
            try:
                doctor = models.Doctor.objects.get(user_id=request.user.id)
                if doctor.status:
                    return redirect('doctor-dashboard')
                else:
                    return render(request,'hospital/doctor_wait_for_approval.html')
            except models.Doctor.DoesNotExist:
                # Doctor record doesn't exist - redirect to home
                return redirect('home')
        elif is_patient(request.user):
            try:
                patient = models.Patient.objects.get(user_id=request.user.id)
                if patient.status:
                    return redirect('patient-dashboard')
                else:
                    return render(request,'hospital/patient_wait_for_approval.html')
            except models.Patient.DoesNotExist:
                # Patient record doesn't exist - redirect to home
                return redirect('home')
        else:
            # User is authenticated but not in any expected group
            # This might be a superuser or staff member not in ADMIN group
            if request.user.is_superuser or request.user.is_staff:
                return redirect('admin-dashboard')
            else:
                return redirect('home')

    except Exception as e:
        # If there's any error, redirect to home page
        print(f"Error in afterlogin_view: {str(e)}")
        return redirect('home')








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required
def admin_dashboard_view(request):
    # Allow access for superusers, staff, or users in ADMIN group
    if not (request.user.is_superuser or request.user.is_staff or (hasattr(request.user, 'groups') and request.user.groups.filter(name='ADMIN').exists())):
        return redirect('adminlogin')

    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()

    # Get department count (unique departments)
    department_count = models.Doctor.objects.values('department').distinct().count()

    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctor_count':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patient_count':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointment_count':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'department_count': department_count,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    try:
        # Get patients pending approval
        patients = models.Patient.objects.filter(status=False)
        print(f"Found {patients.count()} patients pending approval")  # Debug print
        return render(request, 'hospital/admin_approve_patient.html', {'patients': patients})
    except Exception as e:
        print(f"Error in admin_approve_patient_view: {str(e)}")  # Debug print
        # Return a simple error message for now
        return HttpResponse(f"An error occurred: {str(e)}", status=500)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments = models.Appointment.objects.all().filter(status=True).select_related('patientId', 'doctorId')
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.patientId=appointmentForm.cleaned_data['patientId']
            appointment.doctorId=appointmentForm.cleaned_data['doctorId']
            appointment.appointmentDate=appointmentForm.cleaned_data['appointmentDate']
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('/admin-view-appointment/')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False).select_related('patientId', 'doctorId')
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect('/admin-approve-appointment/')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('/admin-approve-appointment/')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    # For cards
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    patientcount = models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id).count()
    appointmentcount = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id).count()
    patientdischarged = models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()
    
    # Get today's queue count for the doctor's department
    today = timezone.now().date()
    queuecount = models.QueueToken.objects.filter(
        created_at__date=today,
        status='waiting',
        department=doctor.department  # Only show queue for doctor's department
    ).count()
    
    # For table in doctor dashboard
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=doctor).order_by('-id').select_related('patientId')
    patientid=[]
    for a in appointments:
        if a.patientId:
            patientid.append(a.patientId.id)

    if patientid:
        patients=models.Patient.objects.all().filter(status=True,id__in=patientid).order_by('-id')
        # Ensure we have the same number of patients as appointments
        patients_list = list(patients)
        appointments_list = list(appointments)

        # If we don't have matching patients for all appointments, log the issue
        if len(patients_list) != len(appointments_list):
            print(f"Warning: Found {len(appointments_list)} appointments but only {len(patients_list)} matching patients")
            print(f"Patient IDs from appointments: {patientid}")
            print(f"Patients found: {[p.id for p in patients_list]}")

        appointments = zip(appointments_list, patients_list)
    else:
        appointments = []
        print("No appointments found for this doctor")
    mydict = {
        'patientcount': patientcount,
        'appointmentcount': appointmentcount,
        'patientdischarged': patientdischarged,
        'queuecount': queuecount,  # Add queue count to context
        'appointments': appointments,
        'doctor': models.Doctor.objects.get(user_id=request.user.id),  # for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True, doctorId=doctor).select_related('patientId')
    patientid=[]
    for a in appointments:
        if a.patientId:
            patientid.append(a.patientId.id)

    if patientid:
        patients=models.Patient.objects.all().filter(status=True,id__in=patientid)
        appointments=zip(appointments,patients)
    else:
        appointments = []
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True, doctorId=doctor).select_related('patientId')
    patientid=[]
    for a in appointments:
        if a.patientId:
            patientid.append(a.patientId.id)

    if patientid:
        patients=models.Patient.objects.all().filter(status=True,id__in=patientid)
        appointments=zip(appointments,patients)
    else:
        appointments = []
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    """Delete a specific appointment"""
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('/doctor-view-appointment/')



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_queue_view(request):
    """View department queue for calling patients"""
    doctor = models.Doctor.objects.get(user_id=request.user.id)

    # Get waiting patients in doctor's department
    waiting_patients = models.QueueToken.objects.filter(
        department=doctor.department,
        status='waiting',
        created_at__date=timezone.now().date()
    ).order_by('created_at').select_related('patient__user')

    # Get currently called patient
    called_patient = models.QueueToken.objects.filter(
        department=doctor.department,
        status='called',
        created_at__date=timezone.now().date()
    ).select_related('patient__user').first()

    mydict = {
        'doctor': doctor,
        'waiting_patients': waiting_patients,
        'called_patient': called_patient,
        'waiting_count': waiting_patients.count(),
    }
    return render(request, 'hospital/doctor_queue.html', context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_call_patient_view(request, token_id):
    """Call next patient in queue"""
    if request.method == 'POST':
        try:
            # Get the token and update status to 'called'
            token = models.QueueToken.objects.get(id=token_id, status='waiting')
            token.status = 'called'
            token.save()

            messages.success(request, f'Patient {token.patient.get_name} (Token #{token.token_number}) has been called.')
        except models.QueueToken.DoesNotExist:
            messages.error(request, 'Token not found or already called.')

    return redirect('doctor-queue')


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_complete_consultation_view(request, token_id):
    """Mark consultation as complete"""
    if request.method == 'POST':
        try:
            # Get the token and update status to 'completed'
            token = models.QueueToken.objects.get(id=token_id, status='called')
            token.status = 'completed'
            token.save()

            messages.success(request, f'Consultation for {token.patient.get_name} (Token #{token.token_number}) marked as complete.')
        except models.QueueToken.DoesNotExist:
            messages.error(request, 'Token not found or not currently called.')

    return redirect('doctor-queue')






#---------------------------------------------------------------------------------
#------------------------ QUEUE MANAGEMENT VIEWS ------------------------------
#---------------------------------------------------------------------------------

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def generate_token(request, patient_id):
    """Generate a queue token for a patient"""
    try:
        patient = models.Patient.objects.get(id=patient_id, user_id=request.user.id)

        # Check if patient already has a token for today
        existing_token = models.QueueToken.objects.filter(
            patient=patient,
            created_at__date=timezone.now().date(),
            status__in=['waiting', 'called']
        ).first()

        if existing_token:
            messages.info(request, f'You already have Token #{existing_token.token_number} for today.')
            return redirect('/patient-dashboard/')

        # Get assigned doctor's department
        department = 'General'
        if patient.assignedDoctorId:
            try:
                doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
                department = doctor.department
            except models.Doctor.DoesNotExist:
                pass

        # Get the next token number for today (department-specific)
        today_tokens = models.QueueToken.objects.filter(
            created_at__date=timezone.now().date(),
            department=department
        ).order_by('-token_number')

        next_number = 1
        if today_tokens.exists():
            next_number = today_tokens.first().token_number + 1

        # Create new token
        token = models.QueueToken.objects.create(
            patient=patient,
            token_number=next_number,
            department=department,
            status='waiting'
        )

        messages.success(request, f'Your queue token #{token.token_number} has been generated successfully for {department} department!')
        return redirect('/patient-dashboard/')

    except models.Patient.DoesNotExist:
        messages.error(request, 'Patient not found.')
        return redirect('/patient-dashboard/')
    except Exception as e:
        messages.error(request, f'Error generating token: {str(e)}')
        return redirect('/patient-dashboard/')


#---------------------------------------------------------------------------------
#------------------------ QUEUE MANAGEMENT VIEWS ------------------------------
#---------------------------------------------------------------------------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def queue_list(request):
    """View all queue tokens for admin/staff"""
    tokens = models.QueueToken.objects.all().order_by('-created_at').select_related('patient__user')

    mydict = {
        'tokens': tokens,
        'tokens_waiting': tokens.filter(status='waiting'),
        'tokens_called': tokens.filter(status='called'),
        'tokens_done': tokens.filter(status='completed'),
        'total_waiting': tokens.filter(status='waiting').count(),
        'total_called': tokens.filter(status='called').count(),
        'total_done': tokens.filter(status='completed').count(),
    }
    return render(request, 'hospital/queue_list.html', context=mydict)


def update_token_status(request, token_id, new_status):
    """Update token status via AJAX or direct call"""
    if request.method == 'POST':
        try:
            token = models.QueueToken.objects.get(id=token_id)
            old_status = token.status
            token.status = new_status
            token.save()

            messages.success(request, f'Token #{token.token_number} status updated from {old_status} to {new_status}.')
        except models.QueueToken.DoesNotExist:
            messages.error(request, 'Token not found.')

    return redirect('queue_list')


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def current_token_view(request):
    """View current active tokens for doctor's department"""
    doctor = models.Doctor.objects.get(user_id=request.user.id)

    current_tokens = models.QueueToken.objects.filter(
        department=doctor.department,
        status__in=['waiting', 'called'],
        created_at__date=timezone.now().date()
    ).order_by('created_at').select_related('patient__user')

    mydict = {
        'current_tokens': current_tokens,
        'waiting_count': current_tokens.filter(status='waiting').count(),
        'called_count': current_tokens.filter(status='called').count(),
        'current': current_tokens.filter(status='called').first(),
    }
    return render(request, 'hospital/current_token.html', context=mydict)


#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)

    # Get current token if exists
    current_token = models.QueueToken.objects.filter(
        patient=patient,
        created_at__date=timezone.now().date(),
        status__in=['waiting', 'called']
    ).order_by('-created_at').first()

    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    'current_token': current_token,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}

    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            # Get the appointment date from form
            appointment_date = appointmentForm.cleaned_data['appointmentDate']

            # Check if appointment date is in the past
            from datetime import date
            if appointment_date < date.today():
                message = "Please select a future date for your appointment."
                mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
                return render(request,'hospital/patient_book_appointment.html',context=mydict)

            # Get selected doctor (now a model instance)
            doctor = appointmentForm.cleaned_data['doctorId']

            # Create appointment object but don't save yet
            appointment=appointmentForm.save(commit=False)
            appointment.patientId = patient  # ForeignKey expects model instance
            appointment.doctorId = doctor    # ForeignKey expects model instance
            appointment.status=False  # Pending approval
            appointment.appointmentDate = appointment_date  # Set the selected date
            appointment.save()

            # Success message
            messages.success(request, f'Appointment booked successfully for {appointment_date} with Dr. {doctor.get_name}! It will be confirmed once approved by the doctor or admin.')

            # Debug: Print the redirect URL
            redirect_url = reverse('patient-view-appointment')
            print(f"DEBUG: Redirecting to: {redirect_url}")
            return redirect('/patient-view-appointment/')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)





@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar

    # Get appointments with related doctor information - use ForeignKey relationship for filtering
    appointments = models.Appointment.objects.all().filter(patientId=patient).select_related('doctorId')

    # Create a list of appointment data with doctor information
    appointment_data = []
    for appointment in appointments:
        doctor_info = None
        if appointment.doctorId:
            doctor_info = {
                'name': appointment.doctorId.get_name,
                'department': appointment.doctorId.department
            }

        appointment_data.append({
            'appointment': appointment,
            'doctor': doctor_info
        })

    return render(request,'hospital/patient_view_appointment.html',{
        'appointment_data': appointment_data,
        'patient': patient
    })



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------

#------------------------ PROFILE VIEWS ------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_profile(request):
    if request.method == 'POST':
        form = forms.AdminProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('/admin-dashboard/')
    else:
        form = forms.AdminProfileForm(instance=request.user)
    return render(request, 'hospital/admin_profile.html', {'form': form})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_profile(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        user_form = forms.DoctorUserForm(request.POST, instance=request.user)
        doctor_form = forms.DoctorForm(request.POST, request.FILES, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('/doctor-dashboard/')
    else:
        user_form = forms.DoctorUserForm(instance=request.user)
        doctor_form = forms.DoctorForm(instance=doctor)
    return render(request, 'hospital/doctor_profile.html', {
        'user_form': user_form,
        'doctor_form': doctor_form
    })

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_profile(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        user_form = forms.PatientUserForm(request.POST, instance=request.user)
        patient_form = forms.PatientForm(request.POST, request.FILES, instance=patient)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('/patient-dashboard/')
    else:
        user_form = forms.PatientUserForm(instance=request.user)
        patient_form = forms.PatientForm(instance=patient)
    return render(request, 'hospital/patient_profile.html', {
        'user_form': user_form,
        'patient_form': patient_form
    })
#------------------------ PROFILE VIEWS END --------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------

