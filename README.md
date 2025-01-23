# BandobastNet
---
E-Bandobast

Team Name: The Team

How our apps works:
* The app is a web application that helps the police department to manage the coordination during large events. We've implemented features like live geolocation tracking, automatic email notifications, and a dashboard for the admin to manage the officers, and our own detailed database for police officers.


How to run the raw source code:
* needs mysql installed.
use sql to create a database called bandobast.
open a terminal, and run the following commands:
1. pip install -r requirements.txt
2. python manage.py loaddata initial_data.json
3. python manage.py makemigrations
4. enter your mysql username and password in the bandobast/settings.py file, line 80.


open another terminal in the same directory where the code is saved.
run python manage.py runserver in one terminal, and ngrok http 8000 in the other terminal.
Copy the ngrok link and paste it in the browser.

emails informing officers about their timings are sent using the google smtp server, for this to work an 'App Password' needs to be generated from the sender's email account.
To generate an App Password, refer: https://support.google.com/mail/answer/185833?hl=en
Once the App Password is generated, replace the 'EMAIL_HOST_PASSWORD' (line 184) in the bandobast/settings.py.

can be accessed as a pwa on the phone by clicking the 'Add to Home Screen' option in the browser.

for geolocation, the officer would need to have the app running and click on the send location button, and the user would be tracked on the map from that point onwards.

Do refer to the demo video!
