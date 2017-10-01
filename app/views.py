# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import wave
import pydub
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from PickupAI.settings import BASE_DIR
from audio_text_parser.audio_text_parser import AudioTextParser


def index(request):
    return render(request, "index.html", {})


@csrf_exempt
def parse_audio_file(request):

    if request.method == 'POST' and request.is_ajax():

        blob_data = request.FILES.get("data")

        tmp_file_path = os.path.join(BASE_DIR, "app", "tmp_files", "tmp_wav_file.wav")

        w = wave.open(os.path.join(os.path.relpath(__file__), "..", "audio_text_parser", "test_files", "recording.wav"), "rb")
        binary_data = w.readframes(w.getnframes())
        w.close()

        output = AudioTextParser(binary_data).parse_audio()
        process_text_service(output)
        dict_parsed_text = json.loads(output)

        # audio_text_path = os.path.join(BASE_DIR, "app", "audio_text_parser", "audio_text_parser.py")
        # output = os.subprocess.check_output(["python", audio_text_path, os.path.join(BASE_DIR, "app", "tmp_files", "output.wav")])
        # print output

        return HttpResponse(status=200, content="Test")


def process_text_service(parsed_text):

    status = parsed_text.get("RecognitionStatus")

    if status == "Success":

        text = parsed_text.get("DisplayText")
        words = text.split(' ')
        print words
        # lookup_list = ["transfer", "savings", "chequing"]
        lookup_list = ["tour", "long"]
        if all(word in words for word in lookup_list):
            print "test"

            # if words.index("savings") < words.index("chequing"):
            #     pass