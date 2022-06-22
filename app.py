from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import numpy as np
import pandas as pd

app = Flask(__name__)                    

@app.route('/')
def home():
  
  return ('hello')

hh =  ''' @app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    try:
        num_media = request.values.get("NumMedia")
        inc = request.values.get("Body","").lower()
        media = request.values.get('MediaContentType0', '')
        phone_number = request.form.get('From')
        
    except (ValueError, TypeError):
        return "Invalid request: invalid or missing NumMedia parameter", 400
    response = MessagingResponse()
    
    if 'hey' in inc:
      
      msg = response.message(inc)
          
    else:
        if media.startswith('image/'):
            file_url = request.values['MediaUrl0']
            msg = response.message('hey'))
            msg.media(file_url)
            
        elif media.startswith('video/'):
            file_url = request.values['MediaUrl0']
            msg = response.message('you sent us this video')
            msg.media(file_url)
            
        else:
            msg = response.message('we dont understand what you have given bro')
          
    return str(response)'''
 
if __name__ == '__main__':
  app.run()

