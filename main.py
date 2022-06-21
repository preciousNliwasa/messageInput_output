from fastapi import FastAPI
#import pickle

app = FastAPI(title = 'Message Input/Output')

#vectorizer = pickle.load(open('vectorizer.pkl','rb'))
#model = pickle.load(open('chatbotModel.pkl','rb'))

@app.get('/',tags = ['Home'])
async def home():
    return 'welcome'

#@app.get('/text_category',tags = ['Text Category'])
#async def text_category(message : str):
    
#    message_transform = vectorizer.transform([message])
    
#    predicted = model.predict(message_transform)
    
#    return predicted[0]

