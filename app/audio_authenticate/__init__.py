import json

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

    identificationProfileId = json.loads(response.text).get("identificationProfileId")
    return identificationProfileId


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
    profile_id_list = []
    url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles"
    headers = {
        'ocp-apim-subscription-key': SUBSCRIPTION_TOKEN,
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers)
    for items in json.loads(response.text):
        profile_id_list.append(items.get('identificationProfileId'))
    return profile_id_list

    return response.text


def identify_user(list_profileids, identify_audio_file):
    url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identify"

    querystring = {
        "identificationProfileIds": list_profileids}

    headers = {
        'host': "westus.api.cognitive.microsoft.com",
        'content-type': "application/octet-stream",
        'ocp-apim-subscription-key': "dc1c63aec7fa4446961f56fba8e1aefa",
        'cache-control': "no-cache",
        'postman-token': "5513c734-afdc-cc69-aa79-9af10f831d9b"
    }

    response = requests.request("POST", url, headers=headers, params=querystring,
                                data=open('../../' + identify_audio_file, 'rb'))
    return response.headers.get('Operation-Location').split('/')[-1]


def auth_user(oper_code, *args):
    url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/operations/933f699e-6f85-4c71-bdf9-e24d8b50799c"

    # querystring = {"operationId": "a137ad81-1659-41c2-bca1-7d3351aad04a"}
    querystring = {"operationId": oper_code}

    headers = {
        'host': "westus.api.cognitive.microsoft.com",
        'ocp-apim-subscription-key': SUBSCRIPTION_TOKEN,
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    resp = json.loads(response.text).get('processingResult')
    print response.text
    try:
        profile_id = resp.get('identifiedProfileId')
        status = resp.get('confidence')
        return {'Confidence': status, 'profile_id': profile_id}
    except AttributeError:
        return 'Not Found'


if __name__ == '__main__':
    # print identify_user(get_all_profiles())
    print auth_user(identify_user(get_all_profiles()), 'auth')
