import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Attendance, ReferencePoint
from django.utils import timezone

from .forms import CustomUserCreationForm

from datetime import datetime, date
from twilio.rest import Client
from django.http import HttpResponse

import pywhatkit
from .utils import is_within_radius

from twilio.base.exceptions import TwilioRestException
import logging


SECRET_KEY = os.environ.get('SECRET_KEY')
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')



def chat_HR(admin='whatsapp:+2347037006829'):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body="Good day HR Mgr \n{} {} just signed in {}!!!".format("first", "second", "third"),
    to=admin
    )
    return "HR chatted!!!"

# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ["TWILIO_ACCOUNT_SID"]
# auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Hello there!",
    from_="whatsapp:+14155238886",
    to="whatsapp:+15005550006",
)

print(message.body)

def twilio(request):
    # chat_HR()
    phone_number = "+2347037006829"
    message = "message"

    pywhatkit.sendwhatmsg_instantly(phone_number, message)
    print("Whatsapp message sent!!!")
    return HttpResponse("Hello, World!")


def check_distance(request):
    result = None

    if request.method == 'POST':
        x = request.POST.get('easting')
        y = request.POST.get('northing')
        print(f"x: {x}, y: {y}")
        easting = float(request.POST.get('easting'))
        northing = float(request.POST.get('northing'))

        # Get the reference point (you might want to select a specific point by id or name)
        reference_point = get_object_or_404(ReferencePoint, id=1)  # Replace with your reference point id

        # Check if the point is within the 5-meter radius
        within_radius = is_within_radius(reference_point.easting, reference_point.northing, easting, northing, radius=5)

        result = "Within 5 meters" if within_radius else "Not within 5 meters"

    return render(request, 'accounts/check_distance.html', {'result': result})




# def check_distance(request, ref_id):
#     reference_point = ReferencePoint.objects.get(id=ref_id)
#
#     # Get easting and northing from request (for example, from query parameters)
#     easting = float(request.GET.get('easting'))
#     northing = float(request.GET.get('northing'))
#
#     # Check if the point is within the 5-meter radius
#     within_radius = is_within_radius(reference_point.easting, reference_point.northing, easting, northing, radius=5)
#
#     return HttpResponse(within_radius)
#     # return JsonResponse({'within_radius': within_radius})



# def check_distance(request, ref_id):
#     reference_point = ReferencePoint.objects.get(id=ref_id)
#
#     # Get latitude and longitude from request (for example, from query parameters)
#     lat = float(request.GET.get('lat'))
#     lon = float(request.GET.get('lon'))
#
#     # Check if the point is within the 5-meter radius
#     within_radius = is_within_radius(reference_point.latitude, reference_point.longitude, lat, lon, radius=5)
#
#     return HttpResponse(within_radius)
#     # return JsonResponse({'within_radius': within_radius})


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

                logger = logging.getLogger(__name__)

                try:
                    client = Client(account_sid, auth_token)
                    message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body="Good day HR Mgr \n{} {} just signed in {}!!!".format(str(user.first_name),
                         str(user.last_name), "remotely or what"),
                    to='whatsapp:+2347037006829',
                    )

                except TwilioRestException as e:
                    # Log the detailed error
                    logger.error(f"Twilio API error: {e.status} - {e.msg}")
                    # Optionally, log the full exception
                    logger.exception("Twilio API call failed.")
                except Exception as e:
                    # Catch other exceptions
                    logger.exception("An unexpected error occurred.")

                # client = Client(account_sid, auth_token)
                # message = client.messages.create(
                # from_='whatsapp:+14155238886',
                # body="Good day HR Mgr \n{} {} just signed in {}!!!".format(str(user.first_name),
                #      str(user.last_name), user_location),
                # to='whatsapp:+2347037006829')

            return redirect('attendance_list')
        else:
            messages.success(request, ("Invalid username or password. Try Again..."))
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
