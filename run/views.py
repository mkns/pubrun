""" All the views code, you won't be surprised to hear """

import uuid
import hashlib
from io import BytesIO
from run.models import Athlete
import qrcode
import qrcode.image.svg
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
        url = "http://www.irreverence.co.uk/pubrun/redirect?data={}{}" \
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
    print(request.GET.get("data"))
    data = request.GET.get("data")
    checksum = data[0:64]
    athlete_id = data[64:]
    print(checksum, athlete_id)
    athlete = Athlete.objects.filter(checksum=checksum).filter(id=athlete_id)
    print(athlete)
    context = {"qr": athlete[0].qrcodexml}
    return render(request, "run/qrcode.html", context)
