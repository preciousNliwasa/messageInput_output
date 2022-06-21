from fastapi import FastAPI
import joblib

app = FastAPI(title = 'Message Input/Output')

#model = joblib.load('chatbot.joblib')
#vectorizer = joblib.load('vectorizer.joblib')

@app.get('/',tags = ['Home'])
async def home():
    return 'welcome'

#@app.get('/text_category',tags = ['Text Category'])
#async def text_category(message : str):
    
#    message_transform = vectorizer.transform([message])
    
#    predicted = model.predict(message_transform)
    
#    return predicted[0]

