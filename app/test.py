import wave
import os
import re
import sys
import django

sys.path.append(os.path.join(os.path.relpath(__file__), "..", ".."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'PickupAI.settings'
django.setup()

from app.models import Person
from audio_text_parser.audio_text_parser import AudioTextParser


def process_text_service(parsed_text):

    status = parsed_text.get("RecognitionStatus")

    if status == "Success":

        text = parsed_text.get("DisplayText")
        words = text.split(' ')
        print words
        lookup_list = ["transfer", "savings", "chequing"]

        if words.index("savings") < words.index("checking"):

            regexp_amt = re.compile(r'\$\d+')
            for word in words:
                if re.match(regexp_amt, word):
                    amt = re.findall("\d+", word)
                    random_person = Person.objects.filter(id=3).first()
                    random_person.savings_amount -= 50
                    random_person.chequing_amount -= 50
                    random_person.save()


if __name__ == "__main__":

    w = wave.open(os.path.join(os.path.relpath(__file__), "..", "audio_text_parser", "test_files", "recording.wav"),
                  "rb")
    binary_data = w.readframes(w.getnframes())
    w.close()

    output = AudioTextParser(binary_data).parse_audio()
    process_text_service(output)
