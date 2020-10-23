from twilio.rest import Client 
  
# Your Account Sid and Auth Token from twilio.com / console 
account_sid = 'AC4a29b32ccd444427b42628d31f54f832'
auth_token = '4cad8d56a82780a34dc1e5c42a9d14a0' ##copy from ssrivas@bt. account
  
client = Client(account_sid, auth_token) 

def send_otp_msg(mobile_no, otp):
    try:
        content = "you otp for dhadkan password reset in this {}".format(otp)
        message = client.messages.create( 
                                    from_='+12317903233', 
                                    body = content, 
                                    to ='+91{}'.format(mobile_no)
                                ) 
        
        print(message.sid) 
        return True
    except:
        return False