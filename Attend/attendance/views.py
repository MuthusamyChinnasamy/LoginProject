from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Atten,Attenwork
from .forms import AttendForm,AttenworkForm
from django.contrib import messages
from .models import Atten
from datetime import datetime,date,timedelta,time
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    if request.method == 'POST':
        # Retrieve selected dropdown value and input value from the request's POST data
        status = request.POST.get('status', '')
        input_value = request.POST.get('input_value', '')

        # Define status messages for different dropdown values
        status_messages = {
            "in": "Login ID: ",
            "lunchin": "Lunchout ID: ",
            "lunchout": "Lunchin ID: ",
            "cpin": "Breakout ID: ",
            "cpout": "Breakin ID: ",
            "out": "Logout ID:"
        }

        data = None
        error_message = None  # Error message

        try:
            if status in status_messages:
                # Retrieve Atten objects from the database with the given Empid
                atten_queryset = Atten.objects.filter(Empid=input_value)
                if atten_queryset.exists():
                    # If Atten objects exist, create an Attenwork object and save it
                    data = status_messages[status] + input_value
                    atten = atten_queryset.first()
                    current_datetime = datetime.now()
                    current_date = current_datetime.date()  # Get the current date
                    current_time = current_datetime.time()

                    attenwork_queryset = Attenwork.objects.filter(Empid=atten, date=current_date)
                    if attenwork_queryset.exists():
                        attenwork = attenwork_queryset.first()
                    else:
                        attenwork = Attenwork(Empid=atten, date=current_date)
                        attenwork.save()

                    if status == "in":
                        if not attenwork.timein:
                            attenwork.timein = current_time
                            error_message = "Login time is recorded Successfully."
                        else:
                            error_message = "Login time is already recorded."
                    elif status == "lunchin":
                        if not attenwork.lunchout:
                            attenwork.lunchout = current_time
                            error_message = "Lunch out time is recorded Successfully."
                        else:
                            error_message = "Lunch out time is already recorded."
                    elif status == "cpin":
                        if not attenwork.breakout:
                            attenwork.breakout = current_time
                            error_message = "Break out time is recorded Successfully."
                        else:
                            error_message = "Break out time is already recorded."
                    elif status == "cpout":
                        if not attenwork.breakin:
                            attenwork.breakin = current_time
                            error_message = "Break in time is recorded Successfully."
                        else:
                            error_message = "Break in time is already recorded."
                    elif status == "lunchout":
                        if not attenwork.lunchin:
                            attenwork.lunchin = current_time
                            error_message = "Lunch in time is recorded Successfully."
                        else:
                            error_message = "Lunch in time is already recorded."
                    elif status == "out":
                        if not attenwork.logout:
                            attenwork.logout = current_time
                            error_message = "Logout time is recorded Successfully."
                        else:
                            error_message = "Logout time is already recorded."
                    else:
                        error_message = "Default time is already recorded."

                    attenwork.save()

                    # Calculate total time
                    total_time = timedelta()
                    if attenwork.timein and attenwork.logout:
                        total_time += datetime.combine(date.today(), attenwork.logout) - datetime.combine(date.today(), attenwork.timein)
                    if attenwork.lunchout and attenwork.lunchin:
                        total_time -= datetime.combine(date.today(), attenwork.lunchin) - datetime.combine(date.today(), attenwork.lunchout)

                    totalhour = total_time.total_seconds() / 3600  # Convert total_time to hours

                    attenwork.totalhour = totalhour  # Assign totalhour value to the Attenwork model field
                    attenwork.save()  # Save the updated Attenwork object

                else:
                    # Create a new Attenwork object with the new values
                    atten = Atten.objects.create(Empid=input_value)
                    current_datetime = datetime.now()
                    current_date = current_datetime.date()  # Get the current date
                    current_time = current_datetime.time()

                    attenwork = Attenwork(Empid=atten, date=current_date)
                    if status == "in":
                        attenwork.timein = current_time
                        error_message = "Login time is recorded Successfully."
                    elif status == "lunchin":
                        attenwork.lunchout = current_time
                        error_message = "Lunch out time is recorded Successfully."
                    elif status == "cpin":
                        attenwork.breakout = current_time
                        error_message = "Break out time is recorded Successfully."
                    elif status == "cpout":
                        attenwork.breakin = current_time
                        error_message = "Break in time is recorded Successfully."
                    elif status == "lunchout":
                        attenwork.lunchin = current_time
                        error_message = "Lunch in time is recorded Successfully."
                    elif status == "out":
                        attenwork.logout = current_time
                        error_message = "Logout time is recorded Successfully."
                    else:
                        error_message = "Invalid status."

                    attenwork.save()

                    totalhour = None

            else:
                data = "Invalid status."
        except Exception as e:
            data = "Error occurred: " + str(e)
            totalhour = None

        context = {
            'data': data,  # Pass the notification message to the template
            'error_message': error_message,  # Pass the error message to the template
            'totalhour': totalhour
        }

        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')

def reg(request):
    if request.method == "POST":
        form = AttendForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. You can log in now!')
            return HttpResponseRedirect('/reg')
    else:
        form = AttendForm()

    return render(request, 'resigter.html', {'form': form})



def alldata(request):
    data=Attenwork.objects.all()
    context={
        "data":data
    }
    return render(request, 'my_template.html', {"data": data})

