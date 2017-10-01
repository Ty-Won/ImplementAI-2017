import traceback
import uuid

import os
import requests
import wave
from argparse import ArgumentError, ArgumentTypeError, ArgumentParser


def main():

    try:

        arg_parser = ArgumentParser(description='Script to parse audio to text')
        arg_parser.add_argument('file_path', type=str, help='Path of WAV file')

        args = arg_parser.parse_args()

        w = wave.open(os.path.join(os.path.relpath(__file__),"..", "test_files", "man1_wb.wav"), "rb")
        binary_data = w.readframes(w.getnframes())
        w.close()

        AudioTextParser(binary_data).parse_audio()

        exit(0)

    except (ArgumentError, ArgumentTypeError, IOError, OSError):
        exit(1)


class AudioTextParser:
    API_LINK = "https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1"

    def __init__(self, audio_binary=None):
        self.audio_binary = audio_binary

    def parse_audio(self):

        access_token = self.get_access_token()
        return self.send_audio_request(access_token)

    def get_access_token(self):

        url = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"

        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'content-length': "0",
            'ocp-apim-subscription-key': "220e566134014bb9b5cd4c4347521aa8"
        }

        response = requests.request("POST", url, headers=headers)

        return response.text

    def send_audio_request(self, access_token):
        # Upload Audio to API

        querystring = {"language": "en-US", "locale": "en-US", "format": "simple", "requestid": uuid.uuid4()}

        headers = {
            'Authorization': 'Bearer ' + access_token,
            'content-type': "audio/wav; codec=""audio/pcm""; samplerate=16000"
        }

        response = requests.request("POST", AudioTextParser.API_LINK, headers=headers, params=querystring,
                                    data=self.audio_binary)

        print response.json()
        return response.json()


if __name__ == "__main__":
    main()
