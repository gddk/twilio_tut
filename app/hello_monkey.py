from flask import Flask, request, redirect, render_template
from twilio.twiml import Response
from twilio.util import TwilioCapability
from secret import (phone_brit, phone_dave, phone_rob, phone_kenna, account_sid, auth_token,
                    phone_m, application_sid)
import re

application = Flask(__name__)
caller_id = phone_m
default_client = 'jenny'


@application.route('/hello-monkey/', methods=['GET', 'POST'])
def hello_monkey():
    """Root handler"""
    people = {
        '{}'.format(phone_dave): 'David',
        '{}'.format(phone_kenna): 'Makenna',
        '{}'.format(phone_brit): 'Britiany',
        '{}'.format(phone_rob): 'Robert',
    }
    name = people.get(request.args.get('From', ''), 'Monkey')
    resp = Response()
    resp.say("Hello " + name)
    resp.play("http://demo.twilio.com/hellomonkey/monkey.mp3")
    with resp.gather(numDigits=1, action="/hello-monkey/handle-key/", method="POST") as g:
        g.say('To speak to a real monkey, press 1. '
              'Press 2 to record your own monkey howl. '
              'Press 3 to talk to customer support. '
              'Press any other key to start over.')
    return str(resp)


@application.route("/hello-monkey/handle-key/", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == "1":
        resp = Response()
        resp.dial(phone_dave)
        resp.say("The call failed, or the party hung up. Goodbye.")
        return str(resp)
    elif digit_pressed == "2":
        resp = Response()
        resp.say("Record your monkey howl after the tone.")
        resp.record(maxLength="30", action="/hello-monkey/handle-recording/")
        return str(resp)
    elif digit_pressed == "3":
        return redirect("/hello-monkey/voice/")
    else:
        return redirect("/hello-monkey/")


@application.route("/hello-monkey/handle-recording/", methods=['GET', 'POST'])
def handle_recording():
    """Play back the caller's recording."""
    recording_url = request.values.get("RecordingUrl", None)
    resp = Response()
    if recording_url:
        resp.say("Thanks for howling... take a listen to what you howled.")
        resp.play(recording_url)
        resp.say("Goodbye.")
    else:
        resp.say("An error has occurred.  Goodbye.")
    return str(resp)


@application.route('/hello-monkey/voice/', methods=['GET', 'POST'])
def voice():
    dest_number = request.values.get('PhoneNumber', None)
    resp = Response()
    with resp.dial(callerId=caller_id) as r:
        if dest_number and re.search(r'^\d{11}$', dest_number):
            r.number(dest_number)
        else:
            r.client(dest_number)
    return str(resp)


@application.route("/hello-monkey/client/", methods=['GET', 'POST'])
def client():
    """Respond to incoming requests"""
    client_name = request.values.get('client', None) or "jenny"
    capability = TwilioCapability(account_sid, auth_token)
    capability.allow_client_outgoing(application_sid)
    capability.allow_client_incoming(client_name)
    token = capability.generate()
    return render_template('client.html', token=token, client_name=client_name)


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')
