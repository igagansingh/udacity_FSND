from twilio.rest import Client
# put your own credentials here
account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)
message = client.messages.create(
  to="+9195822xxxxx",
  from_="+121551xxxx ",
  body="Hey , you're just amazing.")
print message.sid