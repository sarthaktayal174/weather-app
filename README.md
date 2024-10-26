## weather-app
This is a real time weather checking app that updates the data base in real time

It runs by repeatedly sending requests to openweatherapi and updating the daily aggregates in the database
The database we have used is mongodb
processor.py is where all the data processing is done
for an interval mechanism I have used apschedular whic updates the data every five minutes
there is also an alerting system which is triggered when threshhold temp is reached which sends you an sms on your phone
I have used dash as a frontend data visualizer which plots the data on a linegraph

in order to run this you need to feed the openweather_api_key, twilio_auth_token,twilio_sid,and you phone_no in the environment variables in run.py
