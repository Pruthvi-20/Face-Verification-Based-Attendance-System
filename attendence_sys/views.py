from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Student, Attendence
from .filters import AttendenceFilter

# from django.views.decorators import gzip

from .recognizer import Recognizer
from datetime import date

@login_required(login_url = 'login')
def home(request):
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data = request.POST, files=request.FILES)
        # print(request.POST)
        stat = False 
        try:
            student = Student.objects.get(registration_id = request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get('firstname') +" " +studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name + ' was successfully added.')
            return redirect('home')
        else:
            messages.error(request, 'Student with Registration Id '+request.POST['registration_id']+' already exists.')
            return redirect('home')

    context = {'studentForm':studentForm}
    return render(request, 'attendence_sys/home.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'attendence_sys/login.html', context)

@login_required(login_url = 'login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login')
def updateStudentRedirect(request):
    context = {}
    if request.method == 'POST':
        try:
            reg_id = request.POST['reg_id']
            branch = request.POST['branch']
            student = Student.objects.get(registration_id = reg_id, branch = branch)
            updateStudentForm = CreateStudentForm(instance=student)
            context = {'form':updateStudentForm, 'prev_reg_id':reg_id, 'student':student}
        except:
            messages.error(request, 'Student Not Found')
            return redirect('home')
    return render(request, 'attendence_sys/student_update.html', context)

@login_required(login_url = 'login')
def updateStudent(request):
    if request.method == 'POST':
        context = {}
        try:
            student = Student.objects.get(registration_id = request.POST['prev_reg_id'])
            updateStudentForm = CreateStudentForm(data = request.POST, files=request.FILES, instance = student)
            if updateStudentForm.is_valid():
                updateStudentForm.save()
                messages.success(request, 'Updation Success')
                return redirect('home')
        except:
            messages.error(request, 'Updation Unsucessfull')
            return redirect('home')
    return render(request, 'attendence_sys/student_update.html', context)


@login_required(login_url='login')
def takeAttendence(request):
    if request.method == 'POST':
        details = {
            'branch': request.POST['branch'],
            'year': request.POST['year'],
            'section': request.POST['section'],
            'period': request.POST['period'],
            'faculty': getattr(request.user, 'faculty', None)
        }

        if not details['faculty']:
            messages.error(request, "Faculty information not found for the user.")
            return redirect('home')

        # Check if attendance is already recorded for the same date, branch, year, section, and period
        if Attendence.objects.filter(
            date=date.today(),
            branch=details['branch'],
            year=details['year'],
            section=details['section'],
            period=details['period']
        ).exists():
            messages.error(request, "Attendance has already been recorded for this session.")
            return redirect('home')

        # Get students in the specified class
        students = Student.objects.filter(branch=details['branch'], year=details['year'], section=details['section'])

        # Perform face recognition and get recognized student IDs
        recognized_names = Recognizer(details)

        # Mark attendance for each student
        for student in students:
            status = 'Present' if str(student.registration_id) in recognized_names else 'Absent'
            Attendence.objects.create(
                Faculty_Name=details['faculty'],
                Student_ID=str(student.registration_id),
                period=details['period'],
                branch=details['branch'],
                year=details['year'],
                section=details['section'],
                status=status
            )

        # Fetch updated attendance records
        attendences = Attendence.objects.filter(
            date=date.today(),
            branch=details['branch'],
            year=details['year'],
            section=details['section'],
            period=details['period']
        )

        messages.success(request, "Attendance recorded successfully.")
        context = {"attendences": attendences, "ta": True}
        return render(request, 'attendence_sys/attendence.html', context)

    return redirect('home')

@login_required(login_url='login')
def attendance_history(request):
    # Fetch last 5 unique attendance sessions based on date, branch, year, and section
    last_five_attendances = (
        Attendence.objects.values('date', 'branch', 'year', 'section', 'period')
        .annotate(total_students=Count('Student_ID'))
        .order_by('-date', '-time')[:5]  # Fetch latest 5 attendance sessions
    )

    return render(request, "attendance_history.html", {"last_five_attendances": last_five_attendances})


def searchAttendence(request):
    attendences = Attendence.objects.all()
    myFilter = AttendenceFilter(request.GET, queryset=attendences)
    attendences = myFilter.qs
    context = {'myFilter':myFilter, 'attendences': attendences, 'ta':False}
    return render(request, 'attendence_sys/attendence.html', context)


def facultyProfile(request):
    # Check if the user has an associated faculty profile
    faculty = getattr(request.user, 'faculty', None)

    if faculty is None:
        messages.error(request, "Faculty profile not found for this user.")
        return redirect('home')  # Redirect to home or any appropriate page

    form = FacultyForm(instance=faculty)
    context = {'form': form}
    return render(request, 'attendence_sys/facultyForm.html', context)

