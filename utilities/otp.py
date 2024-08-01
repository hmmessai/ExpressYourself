import requests 
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('AFROMESSAGES_TOKEN')
senderId = os.getenv('AFROMESSAGES_SENDER_ID')
# api token

def send_otp(phone_number):                           
# session object
    session = requests.Session()
    # base url
    base_url = 'https://api.afromessage.com/api/challenge'

    # header
    headers = {'Authorization': 'Bearer ' + token}
   
   # request parameters
    to = str(phone_number)
    sender_id = senderId
    pre = "Your OTP is "
    post = ". It will expire after 15 minutes"
    sb = 1
    sa = 0
    ttl = 15 * 60
    len = 5
    t = 1
    # final url
    url = '%s?from=%s&to=%s&pr=%s&ps=%s&sb=%d&sa=%d&ttl=%d&len=%d&t=%d' % (base_url, sender_id, to, pre, post, sb, sa, ttl, len, t)
    # make request
    result = session.get(url, headers=headers)
    # check result
    if result.status_code == 200:
        # request is success. inspect the json object for the value of `acknowledge`
        json = result.json()
        if json['acknowledge'] == 'success':
            # do success
            print('api success')
            return json['response']['code']
        else:
            print(json)
    else:
        # anything other than 200 goes here.
        print('http error ... \ncode: %d \nmsg: %s ') % (result.status_code, result.content)
        raise Exception('URLFailed', result.content)



def verify_phone_number(code, phone_number):
    session = requests.Session()
    # base url
    base_url = 'https://api.afromessage.com/api/verify'
    
    # header
    headers = {'Authorization': 'Bearer ' + token}
    # request parameters
    # Note: You can also use the verification id sent in the challenge request. 
    # Use the `vc` query parameter to verify via verification id.
    to = phone_number
    code = code
    # final url
    url = '%s?to=%s&code=%s' % (base_url, to, code)
    # make request
    result = session.get(url, headers=headers)
    # check result
    if result.status_code == 200:
        # request is success. inspect the json object for the value of `acknowledge`
        json = result.json()
        if json['acknowledge'] == 'success':
            return True
        else:
            return False
    else:
        # anything other than 200 goes here.
        print('http error ... code: %d , msg: %s ') % (result.status_code, result.content)
