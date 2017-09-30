import requests
from PickupAI.config import SUBSCRIPTION_TOKEN

global identificationProfileId


def create_profile():
    url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles"

    payload = "{\r\n  \"locale\":\"en-us\"\r\n}"
    headers = {
        'content-type': "application/json",
        'host': "westus.api.cognitive.microsoft.com",
        'ocp-apim-subscription-key': SUBSCRIPTION_TOKEN,
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    identificationProfileId = response.text['identificationProfileId']
    enroll_user(identificationProfileId)
    return response.text


def enroll_user(identificationProfileId, audio_file):
    url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles/" + identificationProfileId + "/enroll"

    querystring = {"identificationProfileId": identificationProfileId}

    headers = {
        'content-type': "multipart/form-data",
        'ocp-apim-subscription-key': SUBSCRIPTION_TOKEN,
        'cache-control': "no-cache",
    }

    try:
        response = requests.request("POST", url, headers=headers, params=querystring,
                                    data=open(audio_file, 'rb').read())
    except:
        return None

    enroll_operationID = (response.headers).get('Operation-Location').split('/')[1]
    return {'response': response, 'operationID': enroll_operationID}


def get_all_profiles():
    url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles"
    headers = {
        'ocp-apim-subscription-key': SUBSCRIPTION_TOKEN,
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers)

    return response.text

