#!/usr/bin/env python

import httplib2
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

from collections import Counter

# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

label = 'ingress'

agents = []
messageCount = 0
unrelated = 0
token = ''

def gmail():
    # Start the OAuth flow to retrieve credentials
    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
    http = httplib2.Http()

    # Try to retrieve credentials from storage or run the flow to generate them
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid:
        credentials = run(flow, STORAGE, http=http)

    # Authorize the httplib2.Http object with our credentials
    http = credentials.authorize(http)

    # Build the Gmail service from discovery
    return build('gmail', 'v1', http=http)

def getLabelId(label):
    labels = gmail.users().labels().list(userId='me').execute()
    for l in labels['labels']:
        if l['name'] == label:
            return l['id']

def rateLimit(request):
    i=0
    while i < 5:
        try:
            return request
        except httpError:
            print "httpError happened, sleeping {}".format(i+2)
            sleep(i*2)
        i += 1

@rateLimit
def getMessagesByLabel(label, token):
    return gmail.users().messages().list(userId='me', labelIds=label, pageToken=token).execute()

@rateLimit
def getMessageSubject(id):
    msg = gmail.users().messages().get(
                userId='me',
                id=id,
                format='metadata',
                metadataHeaders='Subject').execute()

    try:
        return msg['payload']['headers'][0]['value']

    except:
        raise

gmail = gmail()
labelid = getLabelId(label)

while messageCount < 500:
#while True:
    # this can throw httpError also!
    messages = getMessagesByLabel(labelid, token)
    if messages['messages'] is not None:
        for message in messages['messages']:
            id = message['id']
            print "{} Fetching message {}".format(messageCount,id)
            subject = getMessageSubject(id)
            if (subject[0:20] == "Ingress notification") or (subject[0:23] == "Ingress Damage Report: "):
                agents.append(subject.split()[6])
            else:
                print "Unrelated {}".format(subject[0:30])
                unrelated += 1

            #except HttpError:
            #    print "HttpError, sleeping for 5 seconds"
            #    time.sleep(5)
#
#            except KeyError:
#                print "Apparently not related, id {}".format(id)
#
#            except:
#                # fuck it
#                print "Hmm, something pretty odd must have happened."
#                break
                
            messageCount += 1

        if messages.get('nextPageToken'):
            print "------------------------------------------"
            print "Messages: {}  Unrelated: {}".format(messageCount,unrelated)
            print "Fetching next page: {}".format(messages['nextPageToken'])
            print "------------------------------------------"
            token = messages.get('nextPageToken')
            # very ghetto rate limiting
            time.sleep(2)
        else:
            break

print ("{} Messages, {} Unrelated.".format(messageCount, unrelated))
count = Counter(agents)
n = 100
print("Top {0} destructive agents:".format(n))
for word, count in count.most_common(n):
    print("{0}: {1}".format(word, count))
