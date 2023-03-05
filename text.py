from twilio.rest import Client 

def textReminder(number,message):
    account_sid = 'ACc59fb2191d19d7d2aa667c0968c09640' 
    auth_token = '7ff144b2bbb5c84453b7ed2b615932ca' 
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create(  
                                messaging_service_sid='MG9b40d05faa2615d5c00a573a86593f13', 
                                body=message,      
                                to=number 
                            ) 
    
    print(message.sid)
    