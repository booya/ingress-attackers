A python script to parse ingress emails using the gmail API.  The following steps are required for this to work:

1) Acces the Google Developers Console at https://console.developers.google.com/.
2) Click on "Create Project", give your project a name, and click 'Create'.
3) Once the project has been created, navigate to APIs & Auth -> APIs.  Enable the Gmail API.  You may disable
the other APIs if you wish.
4) Now select "Credentials" and "Create new Client ID" under OAuth. Application type is Web application.  Set the Authorized Redirect URI to http://localhost:8080/.
remainder of the fields don't matter.
5) Click "Download JSON" to get your client ID file.  Place this file into the directory containing this script.
6) Finally, navigate to "Consent Screen".  Select your email address, and enter something in the "Product name" field.

