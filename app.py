import os
from twilio.rest import Client
import csv

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

incoming_phone_numbers = client.incoming_phone_numbers.list()

# Open the CSV files for incoming and outgoing calls in append mode
with open("incoming_calls.csv", "a", newline="") as incoming_file, open(
    "outgoing_calls.csv", "a", newline=""
) as outgoing_file:
    incoming_writer = csv.writer(incoming_file)
    outgoing_writer = csv.writer(outgoing_file)

    # Write the header row to both files
    incoming_field = ["From", "To", "Duration"]
    outgoing_field = ["From", "To", "Duration"]
    incoming_writer.writerow(incoming_field)
    outgoing_writer.writerow(outgoing_field)

    # Iterate through each phone number
    for number in incoming_phone_numbers:
        # For each number, iterate through incoming calls and save data to the incoming calls CSV
        incoming_calls = client.calls.list(status="completed", to=number.phone_number)
        if len(incoming_calls) > 0:
            for call in incoming_calls:
                incoming_writer.writerow([call._from, call.to, call.duration])

        # For each number, iterate through outgoing calls and save data to the outgoing calls CSV
        outgoing_calls = client.calls.list(
            status="completed", from_=number.phone_number
        )
        if len(outgoing_calls) > 0:
            for call in outgoing_calls:
                outgoing_writer.writerow([call._from, call.to, call.duration])

print("Data has been saved to incoming_calls.csv and outgoing_calls.csv")
