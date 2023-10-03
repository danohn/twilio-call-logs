import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

incoming_phone_numbers = client.incoming_phone_numbers.list()

# Iterate through each phone number
for number in incoming_phone_numbers:
    # For each number, iterate through incoming calls
    incoming_calls = client.calls.list(status="completed", to=number.phone_number)
    if len(incoming_calls) > 0:
        print(f"Incoming Calls to {number.phone_number}:")
        for call in incoming_calls:
            print(f"From: {call._from} - To: {call.to} - Duration: {call.duration}")
    # For each number, iterate through outgoing calls
    outgoing_calls = client.calls.list(status="completed", from_=number.phone_number)
    if len(outgoing_calls) > 0:
        print(f"Outgoing Calls from {number.phone_number}:")
        for call in outgoing_calls:
            print(f"From: {call._from} - To: {call.to} - Duration: {call.duration}")
