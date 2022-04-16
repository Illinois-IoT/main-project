from twilio.rest import Client 
import os
 
account_sid = 'ACd211c25f57b7abc3129befca67c1e2d1' 
#auth_token = os.getenv("AUTH_TOKEN")
auth_token = "b6c5071de4147caee6324cfe167dff61"
client = Client(account_sid, auth_token) 

def send_message(message, to_number): 
	message = client.messages.create(
				from_="+19793105290",
                                to= str(to_number),
				body = str(message)
                          ) 
 
print(message.sid)
