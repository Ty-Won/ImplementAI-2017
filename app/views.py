# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from PickupAI.settings import BASE_DIR
from .models import Person

def index(request):
    file = open("../identitydata.csv")
    for user in file:
        person = user.split(',')
        databaseModel = Person.objects.create()
        databaseModel.profile_id = person[0]
        databaseModel.first_name = person[1]
        databaseModel.savings_amount = person[2]
        databaseModel.chequing_amount = person[3]
        databaseModel.sex = person[4]
        databaseModel.age = person[5]
        databaseModel.save()
    file.close()
    return render(request, "index.html", {})


@csrf_exempt
def parse_audio_file(request):

    if request.method == 'POST' and request.is_ajax():

        blob_data = request.FILES.get("data")

        tmp_file_path = os.path.join(BASE_DIR, "app", "tmp_files", "tmp_wav_file.wav")
        path = default_storage.save(tmp_file_path, ContentFile(blob_data.read()))
        print(path)

        return HttpResponse(status=200, content="Test")


def signup(request):
    return render(request, "sign-up.html", {})

