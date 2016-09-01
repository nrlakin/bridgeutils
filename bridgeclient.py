import requests
import json
import os

BRIDGE_URL = "https://webservices.sagebridge.org"
BRIDGE_API_VERSION = "v3"
BRIDGE_ID = "cornell-mhealth-eval"
APP_NAME = "SDL Bridge Test"
APP_VERSION = 1
DEFAULT_EMAIL = os.environ.get("BRIDGE_EMAIL")
DEFAULT_PASSWORD = os.environ.get("BRIDGE_PASSWORD")

SURVEYS = {
    'demographics': '3a572b28-ccaf-44a8-a5a1-7d0f38b73859'
}

class UserSession:
    username = None
    consented = None
    authenticated = None
    roles = None
    firstName = None
    languages = None
    lastName = None
    createdOn = None
    notifyByEmail = None
    sessionToken = None
    environment = None
    email = None
    dataGroups = None
    status = None
    dataSharing = None
    id = None
    sharingScope = None
    attributes = None
    type = None
    signedMostRecentConsent = None
    consentStatuses = None

    def __init__(self, signin_resp):
        self.username = signin_resp.get('username')
        self.consented = signin_resp.get('consented')
        self.authenticated = signin_resp.get('authenticated')
        self.roles = signin_resp.get('roles')
        self.firstName = signin_resp.get('firstName')
        self.languages = signin_resp.get('languages')
        self.lastName = signin_resp.get('lastName')
        self.createdOn = signin_resp.get('createdOn')
        self.notifyByEmail = signin_resp.get('notifyByEmail')
        self.sessionToken = signin_resp.get('sessionToken')
        self.environment = signin_resp.get('environment')
        self.email = signin_resp.get('email')
        self.dataGroups = signin_resp.get('dataGroups')
        self.status = signin_resp.get('status')
        self.dataSharing = signin_resp.get('dataSharing')
        self.id = signin_resp.get('id')
        self.sharingScope = signin_resp.get('sharingScope')
        self.attributes = signin_resp.get('attributes')
        self.type = signin_resp.get('type')
        self.signedMostRecentConsent = signin_resp.get('signedMostRecentConsent')
        self.consentStatuses = signin_resp.get('consentStatuses')

    def __repr__(self):
        return '<Bridge UserSession %s (%s)>' % (str(self.sessionToken), str(self.email))

userSession = None

def pretty_json(json_body):
    return json.dumps(json_body, sort_keys=True, indent=4, separators=(',', ': '))

def signIn(email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD):
    global userSession
    body = {"study":BRIDGE_ID, "email":email, "password":password}
    endpoint = "/".join([BRIDGE_URL, BRIDGE_API_VERSION, "auth", "signIn"])
    resp = requests.post(endpoint, json=body)
    userSession = UserSession(resp.json())
    return userSession

def getSurvey(survey_name):
    if userSession is None:
        signIn()
    headers = {"Bridge-Session": userSession.sessionToken,
                "User-Agent": "/".join([APP_NAME, str(APP_VERSION)])}
    endpoint = "/".join([BRIDGE_URL, "v3", "surveys", SURVEYS[survey_name], \
                            "revisions", "published"])
    return requests.get(endpoint, headers=headers)

def getSurveyJson(survey_name):
    response = getSurvey(survey_name)
    if response.status_code != 200:
        print("Failed to retrieve survey. Server response: %d" % response.status_code)
        return
    file_name = survey_name+'.json'
    with open(file_name, 'w') as f:
        f.write(pretty_json(response.json()))
    print("Created %s." % file_name)
