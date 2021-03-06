""" All the views code, you won't be surprised to hear """

import uuid
import hashlib
import datetime
import configparser
import os
import ast
from io import BytesIO
from run.models import Athlete, Runs
import qrcode
import qrcode.image.svg
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

@login_required
def index(request):
    """ Front page """
    context = {}
    response = render(request, "run/index.html", context)

    if request.user.is_authenticated:
        print("AUTHENTICATED")
    else:
        print("NOT AUTHENTICATED")

    return response

@login_required
def generate_qrcodes(request):
    """ For all users without a checksum, generate one and the QR code """
    context = {}
    print("First, let's see whether we have any to generate")

    athletes = Athlete.objects.filter(checksum__isnull=True)

    for athlete in athletes:
        print(athlete, athlete.id, athlete.email, athlete.checksum)
        uuid_bytes = uuid.uuid4().bytes
        checksum = hashlib.sha256(uuid_bytes).hexdigest()
        print(checksum)
        athlete.checksum = checksum
        url = "https://mkns.pythonanywhere.com/run/view_athlete_details?data={}{}" \
            .format(athlete.checksum, athlete.id)
        print(url)

        stream = BytesIO()
        img = qrcode.make( url, image_factory=qrcode.image.svg.SvgImage)
        img.save(stream)
        context = {"qr": stream.getvalue().decode() }

        athlete.qrcodexml = stream.getvalue().decode()
        athlete.save()

    return render(request, "run/qrcodes_generated.html", context)

@login_required
def all_runners(request):
    """ Show a list of all runners """
    athletes = Athlete.objects.all()
    context = {"athletes": athletes}
    return render(request, "run/all_runners.html", context)

# Deliberately NOT needing a login, so users can see their QR codes
def view_qr_code(request):
    """ For a Athlete to view their QR code """
    athlete = get_athlete_from_data(request.GET.get("data"))
    context = {"qr": athlete.qrcodexml}
    return render(request, "run/qrcode.html", context)

@login_required
def view_athlete_details(request):
    """
    From scanning the QR code, the URL will bring us here.
    This will allow admins to confirm who the person is, and
    provide a button or link to confirm that the person has
    indeed turned up for a run, if they have registered
    """
    athlete = get_athlete_from_data(request.GET.get("data"))
    context = {"athlete": athlete}

    today = datetime.date.today()
    run = Runs.objects.filter(athlete=athlete).filter(date=today)
    if run.count() == 1:
        this_run = run[0]
        this_run.status = "arrived"
        this_run.save()
        context['run'] = this_run
    print(run)

    return render(request, "run/view_athlete_details.html", context)

def get_athlete_from_data(data):
    """
    the 'data' is the combination of checksum and athlete id,
    and this method merely gets the Athlete from the db
    """
    print("get_athlete_from_data() received data of [{}]".format(data))
    checksum = data[0:64]
    athlete_id = data[64:]
    athlete = Athlete.objects.filter(checksum=checksum).filter(id=athlete_id)
    print(athlete.count())
    if athlete.count() == 1:
        # TODO: I need to put an else block in here
        print(athlete[0].id, athlete[0].name, athlete[0].email, athlete[0].checksum)
        return athlete[0]
    return False

def register_for_run(request):
    """ Show form so people can say they are coming to run """
    dates = get_next_pubrun_dates()
    config = get_config()
    times = get_times_from_config(config)
    context = {'dates': dates, "times": times}
    print("register_for_run({},{})".format(dates, times))

    return render(request, "run/register_for_run.html", context)

def get_next_pubrun_dates():
    """ Helper method to get the dates for the next week's pubruns """
    today = datetime.date.today()
    tuesday = today + datetime.timedelta( (1-today.weekday()) % 7 )
    sunday = today + datetime.timedelta( (6-today.weekday()) % 7 )
    dates = [tuesday, sunday]
    dates.sort()
    return dates

def add_athlete_to_run(request):
    """ Take the form contents and add a row to the Runs table """
    email = request.POST.get("email")
    date = request.POST.get("date")
    time = request.POST.get("time")
    print("add_athlete_to_run({}, {}, {})".format(email, date, time))

    athletes = Athlete.objects.filter(email=request.POST.get("email"))
    if athletes.count() != 1:
        print("The number of athletes returned was {}".format(athletes.count()))
        return False # TODO do something better
    athlete = athletes[0]
    print(athlete, athlete.id)

    try:
        run = Runs.objects.create(athlete=athlete, date=date,
            time=time, status="registered")
        run.save()
    except IntegrityError as error:
        print("Ouch... they probably already registered? {}".format(error))

    # context = {}
    # Change this to call show_registered_runners()
    return show_registered_runners(request)

def show_registered_runners(request):
    """ Show people who have registered to run at an event """
    today = datetime.date.today()
    runs = Runs.objects.filter(date__gte=today)
    context = {'runs': runs, "today": today}
    return render(request, "run/show_registered_runners.html", context)

def get_config():
    """ Gets the config file contents """
    config = configparser.ConfigParser()
    dir_name = os.path.dirname(__file__)
    config_file = os.path.join(dir_name, 'pubrun.conf')
    # print(config_file)
    config.read(config_file)
    return config

def get_times_from_config(config):
    """ Gets the list of available run times from the config object """
    times = ast.literal_eval(config.get("default", "times"))
    return times

@login_required
def populate_test_data(request):
    athletes = Athlete.objects.all()
    today = datetime.date.today() # because frankly, for tests, we don't care if it isn't a Sun/Tue
    r = Runs(athlete=athletes[0], date=today, time="18:00", status="registered")
    r.save()
    r = Runs(athlete=athletes[1], date=today, time="18:00", status="registered")
    r.save()
    r = Runs(athlete=athletes[3], date=today, time="18:10", status="registered")
    r.save()
    r = Runs(athlete=athletes[4], date=today, time="18:20", status="registered")
    r.save()
    return show_registered_runners(request)
