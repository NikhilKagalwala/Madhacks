from twilio.rest import Client 
 
account_sid = 'ACc59fb2191d19d7d2aa667c0968c09640' 
auth_token = '74b032235d7e4af24bc17af42c501d12' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create(  
                              messaging_service_sid='MG9b40d05faa2615d5c00a573a86593f13', 
                              body='hello',      
                              to='+16086365922' 
                          ) 
 
print(message.sid)