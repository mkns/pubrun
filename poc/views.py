""" All the views code, you won't be surprised to hear """

import uuid
import hashlib
from io import BytesIO
from poc.models import Runner
import qrcode
import qrcode.image.svg
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    """ Front page """
    context = {}
    response = render(request, "poc/index.html", context)

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

    runners = Runner.objects.filter(checksum__isnull=True)

    for runner in runners:
        print(runner, runner.id, runner.email, runner.checksum)
        uuid_bytes = uuid.uuid4().bytes
        checksum = hashlib.sha256(uuid_bytes).hexdigest()
        print(checksum)
        runner.checksum = checksum
        url = "http://www.irreverence.co.uk/pubrun/redirect?data={}{}" \
            .format(runner.checksum, runner.id)
        print(url)

        stream = BytesIO()
        img = qrcode.make( url, image_factory=qrcode.image.svg.SvgImage)
        img.save(stream)
        context = {"qr": stream.getvalue().decode() }

        runner.qrcodexml = stream.getvalue().decode()
        runner.save()

    return render(request, "poc/qrcodes_generated.html", context)

@login_required
def all_runners(request):
    """ Show a list of all runners """
    runners = Runner.objects.all()
    context = {"runners": runners}
    return render(request, "poc/all_runners.html", context)

# Deliberately NOT needing a login, so users can see their QR codes
def view_qr_code(request):
    """ For a Runner to view their QR code """
    print(request.GET.get("data"))
    data = request.GET.get("data")
    checksum = data[0:64]
    runner_id = data[64:]
    runner = Runner.objects.filter(checksum=checksum).filter(id=runner_id)
    print(runner)
    context = {"qr": runner[0].qrcodexml}
    return render(request, "poc/qrcode.html", context)
