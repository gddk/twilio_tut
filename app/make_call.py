# Download the library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
from secret import account_sid, auth_token, phone_brit, phone_dave, phone_m

# Get these credentials from http://twilio.com/user/account
client = TwilioRestClient(account_sid, auth_token)
print('here1')  
print(account_sid, auth_token, phone_dave, phone_m)

# Make the call
call = client.calls.create(to=phone_dave,  # Any phone number
                           from_=phone_m, # Must be a valid Twilio number
                           url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
print(call.sid)
