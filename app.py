from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pickle


app = Flask(__name__)


GOOD_BOY_URL = (
    "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-1.2.1"
    "&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"
)

    
vectorizer = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('chatbotModel.pkl','rb'))

def text_category(message):
    
    message_transform = vectorizer.transform([message])
    
    predicted = model.predict(message_transform)
    
    return predicted

@app.route("/")
def home():
    
    return ('welcome')

@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    try:
        num_media = int(request.values.get("NumMedia"))
        inc = request.values.get("Body","").lower()
        phone_number = request.form.get('From')
        
    except (ValueError, TypeError):
        return "Invalid request: invalid or missing NumMedia parameter", 400
    response = MessagingResponse()
    if not num_media:
        
        msg = response.message(text_category(str(inc)))
    else:
        msg = response.message("G,Thanks for the image. Here's one for you!")
        msg.media(GOOD_BOY_URL)
    return str(response)


if __name__ == "__main__":
    app.run()
