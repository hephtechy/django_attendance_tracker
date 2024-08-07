import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Attendance
from django.utils import timezone

from .forms import CustomUserCreationForm

from datetime import datetime, date
from twilio.rest import Client
from django.http import HttpResponse

# SECRET_KEY = os.environ.get('SECRET_KEY')
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')

def chat_HR(admin='whatsapp:+2347037006829'):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body="Good day HR Mgr \n{} {} just signed in {}!!!".format("first", "second", "third"),
    to=admin
    )
    # return "HR chatted!!!"

def twilio(request):
    chat_HR()
    return HttpResponse("Hello, World!")

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tests')
            # return redirect('attendance_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def tests(request):
    # date=datetime.date()
    date=timezone.now().date()
    print("Date: ", date)
    sign_in_time=timezone.now().strftime('%I:%M %p')
    # # sign_in_time=datetime.now().strftime('%I:%M %p')
    # # print("Sign_in_time:", sign_in_time)
    # data = [sign_in_time, date]
    # return render(request, "accounts/tests.html", {'data': data})

    users = CustomUser.objects.all()
    return render(request, "accounts/tests.html", {'users': users})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # print("User is", user)
        # date=timezone.now().date()
        # print("Today's date: ", date)
        # print("   User's attendance status is: ", Attendance.objects.filter(user=user,date=timezone.now().date()))

        if user is not None:
            # Check if user is yet to sign-in today before creating Log instance
            if not Attendance.objects.filter(user=user,date=timezone.now().date()):
                Attendance.objects.create(
                    user=user,
                    date=timezone.now().date())
                # print("TODAY\'S REGISTRATION DONE!!!")

                client = Client(account_sid, auth_token)
                message = client.messages.create(
                from_='whatsapp:+14155238886',
                body="Good day HR Mgr \n{} {} just signed in {}!!!".format(str(user.first_name),
                     str(user.last_name), "remotely or what"),
                to='whatsapp:+2347037006829')

                # client = Client(account_sid, auth_token)
                # message = client.messages.create(
                # from_='whatsapp:+14155238886',
                # body="Good day HR Mgr \n{} {} just signed in {}!!!".format(str(user.first_name),
                #      str(user.last_name), user_location),
                # to='whatsapp:+2347037006829')

            return redirect('attendance_list')
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))
        return redirect('attendance_list')
    return render(request, 'registration/login.html')





# def sign_out(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         print("Username: ", username)
#         print("Password: ", password)
#         print(request.user, "is is_authenticated", user)
#         if user is not None:
#         # if request.user.is_authenticated:
#             try:
#                 # attendance = Attendance.objects.get(
#                 #     user=request.user,
#                 #     date=timezone.now().date()
#                 # )
#                 if Attendance.objects.filter(user=user,date=timezone.now().date()):
#                     print(user.username, "is registered today")
#
#                     # if not Attendance.objects.filter(user=request.user,date=timezone.now().date()):
#
#                     attendance = Attendance.objects.get(
#                         user=user,
#                         date=timezone.now().date()
#                         )
#                     # attendance.sign_out_time = timezone.now()
#                     attendance.sign_out_time = datetime.now().time()
#                     attendance.save()
#                     print("SIGN-OUT TIME FOR TODAY REGISTERED")
#                     print("Sign_Out Type: ", type(attendance.sign_out_time))
#                     print("Sign_in Type: ", type(attendance.sign_in_time))
#                 else:
#                     messages.success(request, ("You have not signed-in today."))
#             except Attendance.DoesNotExist:
#                 pass
#             return redirect('attendance_list')
#     return render(request, 'accounts/sign_out.html')

def sign_out(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the POST data is being retrieved correctly
        # print(f"Username: {username}, Password: {password}")

        user = authenticate(request, username=username, password=password)

        # Debugging the authenticate function
        if user is not None:
            print(f"Authenticated user: {user.username}")

            try:
                # Check if the user has already signed in today
                if Attendance.objects.filter(user=user, date=timezone.now().date()).exists():
                    attendance = Attendance.objects.get(user=user, date=timezone.now().date())
                    if attendance.sign_out_time == None:
                        attendance.sign_out_time = datetime.now().time()
                        attendance.save()
                        print("Sign-out time for today registered.")
                else:
                    messages.error(request, "You have not signed-in today.")
            except Attendance.DoesNotExist:
                messages.error(request, "Attendance record does not exist.")
            # return redirect('attendance_list')
        else:
            messages.error(request, "Invalid username or password.")
        return redirect('attendance_list')

    return render(request, 'accounts/sign_out.html')

def attendance_list(request):
    if request.user.is_authenticated:
        attendances = Attendance.objects.all()
        attendances = Attendance.objects.filter(date=timezone.now().date())
        return render(request, 'accounts/new_attendance_list.html', {'attendances': attendances})
    return redirect('login')
