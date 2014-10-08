ingress-attackers
====
A python script to parse ingress emails using the gmail API.  The following steps are required for this to work:

# Installation
## Configure python environment
Clone the git repository:
    `user@host:~/work$ git clone git@github.com:booya/ingress-attackers.git`

Create virtualenv
    `user@host:~/work$ virtualenv ingress-attackers`

## Configure Gmail API
1. Acces the Google Developers Console at https://console.developers.google.com/.
1. Click on "Create Project", give your project a name, and click 'Create'.
1. Once the project has been created, navigate to APIs & Auth -> APIs.  Enable the Gmail API.  You may disable the other APIs if you wish.
1. Now select "Credentials" and "Create new Client ID" under OAuth. Application type is Web application.  Set the Authorized Redirect URI to http://localhost:8080/. The remainder of the fields don't matter.
1. Click "Download JSON" to get your client ID file.  Place this file into the directory containing this script.
1. Finally, navigate to "Consent Screen".  Select your email address, and enter something in the "Product name" field.

