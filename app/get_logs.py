from twilio.rest import TwilioRestClient
from secret import account_sid, auth_token 

client = TwilioRestClient(account_sid, auth_token)

for call in client.calls.list():
    print('{start}-{end} {direction} {status} {fromN} {to}'.format(
        start=call.start_time, end=call.end_time, direction=call.direction, status=call.status,
        fromN=call.from_formatted, to=call.to_formatted
    ))
