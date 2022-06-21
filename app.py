from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import pickle
import numpy as np
from io import BytesIO
from PIL import Image
import pandas as pd

app = Flask(__name__)                    

@app.route('/')
def home():
  return ('hello')

bird = "https://49t059.deta.dev/stream/birdtensor.jpg"
zuki = "https://49t059.deta.dev/stream/zuki.jpg"
gh = "https://49t059.deta.dev/stream/gh.jpg"
know_api= "https://r1lp8q.deta.dev/know/"

def post_photo(url):
  rr = requests.get(url)
  img = Image.open(BytesIO(rr.content))
  return str(type(img)) + 'was submitted'

from skimage.transform import  resize

@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    try:
        num_media = request.values.get("NumMedia")
        inc = request.values.get("Body","").lower()
        media = request.values.get('MediaContentType0', '')
        phone_number = request.form.get('From')
        
    except (ValueError, TypeError):
        return "Invalid request: invalid or missing NumMedia parameter", 400
    response = MessagingResponse()
    
    # api output to get all plant diseases
    outputt = requests.get(url = "https://1atqmr.deta.dev/get_all_plant_diseases/")
    dff = pd.DataFrame(outputt.json()['_items'])
    
    # api output to get all plant diseases (chichewa)
    output5 = requests.get(url = "https://1atqmr.deta.dev/nthenda_zonse/")
    df5 = pd.DataFrame(output5.json()['_items'])
    
    # api output to get all animal diseases (chichewa)
    output6 = requests.get(url = "https://1atqmr.deta.dev/nthenda_zonse_za_ziweto/")
    df6 = pd.DataFrame(output6.json()['_items'])
    
    # api output to get all animal diseases 
    outputt2 = requests.get(url = "https://1atqmr.deta.dev/get_all_animal_diseases/")
    dff2 = pd.DataFrame(outputt2.json()['_items'])
    
    # api output to get user current languange of choice
    output_lan = requests.get(url = 'https://lkdzzx.deta.dev/get_user_current_language/')
    dff3 = pd.DataFrame(output_lan.json()['_items'])
    
    output_region = requests.get(url = 'https://lkdzzx.deta.dev/get_shop_region/')
    dffregion = pd.DataFrame(output_region.json()['_items'])
    
    # api to get user current operation
    output_op = requests.get(url = 'https://lkdzzx.deta.dev/get_user_current_operation/')
    dff4 = pd.DataFrame(output_op.json()['_items'])
    
    # api to access animals database
    output7 = requests.get(url = "https://1atqmr.deta.dev/get_animals/")
    dff7 = pd.DataFrame(output7.json()['_items'])
    
    # api to access crops database
    output8 = requests.get(url = "https://1atqmr.deta.dev/get_crops/")
    dff8 = pd.DataFrame(output8.json()['_items'])
    
    # api to access zomera database
    output9 = requests.get(url = "https://1atqmr.deta.dev/zomera_zonse/")
    dff9 = pd.DataFrame(output9.json()['_items'])
    
    # api to access ziweto database
    output10 = requests.get(url = "https://1atqmr.deta.dev/ziweto_zonse/")
    dff10 = pd.DataFrame(output10.json()['_items'])
    
    output11 = requests.get(url = "https://1atqmr.deta.dev/all_shops/")
    dfff11 = pd.DataFrame(output11.json()['_items'])
    
    output12 = requests.get(url = "https://1atqmr.deta.dev/get_products/")
    dfff12 = pd.DataFrame(output12.json()['_items'])
    
    
    if not int(num_media):
      
        # intro ,default language = eng,
        if ('hello' in inc) | ('hi' in inc) | ('lange' in inc) :
          msg = response.message("----------------LANGUAGE-------------------- \n Use Codes given to choose an option \n --------------------------------------------------- \n ENG -- english \n CHW -- chichewa \n VN -- audio \n ------------------------------------------------------")
        
        # chichewa (language change)
        elif 'langc' in inc:
           msg = response.message("---------------CHIYANKHULO------------------ \n gwiritsani maletala akumazele kuti musankhe \n ---------------------------------------------------- \n ENG -- english \n CHW -- chichewa \n VN -- audio \n --------------------------------------------------------")
        
        # changing to english
        elif ("eng" in inc) | ('chl' in inc):
          
          # updating to english if language was in chichewa
          if np.any(dff3.user_number.values == phone_number):
             requests.put(url = 'https://lkdzzx.deta.dev/update_language/',params = {'key':dff3.loc[dff3['user_number'] == phone_number,'key'].values[0],'user_number':phone_number,'lan' : 'english'})  
              
          else:
            # registering a new number in english
            requests.post(url = 'https://lkdzzx.deta.dev/language_change/',params = {'user_number':phone_number,'lan' : 'english'})
            
          msg = response.message("----------------CHANNEL------------------\n  Use Codes given to choose an option\n----------------------------------------------------- \n GOPU -- Go Public \n GOPR -- Go Private \n --------------------------------------------- \n LANGE -- Change Language")
        
        elif (('gopu' in inc) | ('mn' in inc)) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          msg = response.message("----------------MAIN MENU------------------\n  Use Codes given to choose an option\n----------------------------------------------------- \n KNWD -- know about diseases \n KNWP -- know about plants \n KNWA -- know about animals \n KNWS -- know about shops \n KNWM -- know about manure \n KNWMA -- know about markets \n -------------------------------------------- \n CHL -- change channel ")
          
        # knowing about diseases (english)
        elif (('knwd' in inc) | ('dsm' in inc)) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
                 
          msg = response.message("----------DISEASE MENU------------ \n --------------------------------------------\n PLT -- plant diseases \n ANM -- animal diseases \n ------------------------------------------------ \n MN -- to main menu")
        
        # knowing about plant diseases (english)
        elif ('plt' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          output = requests.get(url = "https://1atqmr.deta.dev/get_all_plant_diseases/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message('------PLANT DISEASES MENU---------- \n ---------------------------------------------- \n' + str(df[['Code','Disease']]) + '\n ' + '------------------------------------------------ \n DSM -- to diseases Menu')
        
        # description of choosen plant disease (english)  
        elif (np.any(dff.Code.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          pld_D = dff.loc[dff['Code'] == inc,'Description'].values
          msg = response.message(str(pld_D[0]))
        
        # knowing about animal diseases (english)
        elif ('anm' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          output = requests.get(url = "https://1atqmr.deta.dev/get_all_animal_diseases/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message('------ANIMAL DISEASES MENU---------- \n ---------------------------------------------- \n' + str(df[['Code','Disease']]) + '\n ' + '------------------------------------------------ \n DSM -- to diseases Menu')
         
        # description of choosen animal disease (english)
        elif (np.any(dff2.Code.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          anm_D = dff2.loc[dff2['Code'] == inc,'Description'].values
          msg = response.message(str(anm_D[0]))
         
        # knowing about crops
        elif ('knwp' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          
          output = requests.get(url = "https://1atqmr.deta.dev/get_crops/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message("----------CROPS MENU------------ \n --------------------------------------------\n" + str(df[['Code','Crop']]) + " ------------------------------------------------ \n MN -- to main menu")
        
        # description of choosen crop
        elif (np.any(dff8.Code.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          crops = dff8.loc[dff8['Code'] == inc,'Description'].values
          msg = response.message(str(crops[0]))
        
        # knowing about animals
        elif ('knwa' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          
          output = requests.get(url = "https://1atqmr.deta.dev/get_animals/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message("----------ANIMALS MENU------------ \n --------------------------------------------\n" + str(df[['Code','Animal']]) + " ------------------------------------------------ \n MN -- to main menu")
        
        # description of the selected animal
        elif (np.any(dff7.Code.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          animals = dff7.loc[dff7['Code'] == inc,'Description'].values
          msg = response.message(str(animals[0]))
        
        # knowing about shops
        elif (('knws' in inc) | ('reg' in inc)) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          msg = response.message("--------------REGION-------------------- \n ------------------------------------------- \n NRT -- Northen \n CENTR -- Central \n STH -- Southern \n -------------------------------------------- \n MN -- to main menu")
        
        elif ('nrt' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):            
          output = requests.get(url = "https://1atqmr.deta.dev/all_shops/")
          dff = pd.DataFrame(output.json()['_items'])
          df = dff.loc[dff['Region'] == 'north']
          dist4 = pd.DataFrame({'District':df.District.value_counts().index.values})
          msg = response.message("----------DISTRICT MENU------------ \n --------------------------------------------\n" + str(dist4) + "\n " + "---------------------------------------- \n REG -- to region menu")
          
        elif ('centr' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          output = requests.get(url = "https://1atqmr.deta.dev/all_shops/")
          dff = pd.DataFrame(output.json()['_items'])
          df = dff.loc[dff['Region'] == 'central']
          dist4 = pd.DataFrame({'District':df.District.value_counts().index.values})
          msg = response.message("----------DISTRICT MENU------------ \n --------------------------------------------\n" + str(dist4) + "\n " + "---------------------------------------- \n REG -- to region menu")
         
        elif ('sth' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          output = requests.get(url = "https://1atqmr.deta.dev/all_shops/")
          dff = pd.DataFrame(output.json()['_items'])
          df = dff.loc[dff['Region'] == 'south']
          dist4 = pd.DataFrame({'District':df.District.value_counts().index.values})
          msg = response.message("----------DISTRICT MENU------------ \n -------------------------------------------\n" + str(dist4) + "\n " + "---------------------------------------- \n REG -- to region menu")
          
        elif (np.any(dfff11.District.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          #output = requests.get(url = "https://1atqmr.deta.dev/all_shops/")
          #df = pd.DataFrame(output.json()['_items'])
          shop = dfff11.loc[dfff11['District'] == inc,'Shop'].values
          df = pd.DataFrame({'Shops':shop})
          msg = response.message("-----------------SHOPS MENU----------------- \n " + str(df) + "\n ---------------------------------------- \n REG -- to region menu")
          
        #animals = dfff11.loc[dfff11['District'] == inc,'Description'].values
        #msg = response.message(str(animals[0])) 
         
        elif (np.any(dfff11.Shop.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
          shop_descr = dfff11.loc[dfff11['Shop'] == inc,'Description']
          output = requests.get(url = "https://1atqmr.deta.dev/get_products/")
          df = pd.DataFrame(output.json()['_items'])
          products = df.loc[df['Shop'] == inc]
          msg = response.message("-------------------{0}---------------------- \n ".format(inc) + str(shop_descr.values[0]) + "\n ----------------------------------------------- \n " + str(products[["Product","Price"]]) + " \n ---------------------------------------")
        
         
        #elif ('scoh' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
        #  output = requests.get(url = "https://qne10u.deta.dev/get_schools/")
        #  df = pd.DataFrame(output.json()['_items'])
        #  msg = response.message("----------SCHOOLS MENU------------ \n --------------------------------------------- \n " + str(df[['School']]) + " \n ------------------------------------------------ \n MPN -- to main menu")
        
        #elif (np.any(dfffscho.School.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'english'):
        #  school_descr = dfffscho.loc[dfffscho['School'] == inc,'Description']
        #  school_contact = dfffscho.loc[dfffscho['School'] == inc,'Contact']
        #  output = requests.get(url = "https://qne10u.deta.dev/get_topics")
        #  df = pd.DataFrame(output.json()['_items'])
        #  topics = df.loc[df['School'] == inc]
        #  msg = response.message("-------------------{0}---------------------- \n ".format(inc) +  str(school_contact.values[0]) + '\n' + str(school_descr.values[0]) + "\n ----------------------------------------------- \n " + str(topics[["Topic","Description"]]) + " \n ---------------------------------------")
        
        # changing to chichewa
        elif ('chw' in inc) | ('njr' in inc):
          
          # updating lan to chichewa
          if np.any(dff3.user_number.values == phone_number):
            requests.put(url = 'https://lkdzzx.deta.dev/update_language/',params = {'key':dff3.loc[dff3['user_number'] == phone_number,'key'].values[0],'user_number':phone_number,'lan' : 'chichewa'}) 
           
          else:
            # lan to chichewa
            requests.post(url = 'https://lkdzzx.deta.dev/language_change/',params = {'user_number':phone_number,'lan' : 'chichewa'})
            
          msg = response.message("-----------NJIRA------------\n  gwirisani maletala akumazele kuti musankhe \n----------------------------------------------------- \n gopu -- mauthenga a poyera  \n gopr -- mauthenga a puraiveti \n -------------------------------------------- \n LANGC -- kusintha chiyankhulo")
        
        elif (('gopu' in inc) | ('tsam' in inc)) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          msg = response.message("-----------TSAMBA LALIKULU------------\n  gwirisani maletala akumazele kuti musankhe \n----------------------------------------------------- \n KNWD -- dziwani za matenda \n KNWP -- dziwani za zomera \n KNWA -- dziwani za nyama \n KNWS -- dziwani za mashopu \n KNWM -- dziwani za manyowa \n KNWMA -- dziwani za misika \n -------------------------------------------- \n NJR -- kusintha njira")
        
        # knowing about diseases (chichewa)
        elif (('knwd' in inc) | ('tsaz' in inc)) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          msg = response.message("--------TSAMBA LA MATENDA---------- \n --------------------------------------------\n PLT -- matenda a zomera \n ANM -- matenda a nyama \n ------------------------------------------------ \n TSAM -- tsamba lalikulu")
        
        # knowing about plant disease (chichewa)
        elif ('plt' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          output = requests.get(url = "https://1atqmr.deta.dev/nthenda_zonse/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message('--TSAMBA LA MATENDA A ZOMERA-- \n ---------------------------------------------- \n' + str(df[['Letala','Matenda']]) + '\n ' + '------------------------------------------------ \n TSAZ -- tsamba la matenda')
        
        # description of plant diseases (chichewa)
        elif (np.any(df5.Letala.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          pld_D = df5.loc[df5['Letala'] == inc,'Kulongosola'].values
          msg = response.message(str(pld_D[0]))
         
        # knowing about animal diseases (chichewa)
        elif ('anm' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          output = requests.get(url = "https://1atqmr.deta.dev/nthenda_zonse_za_ziweto/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message('TSAMBA LA MATENDA A ZIWETO \n ---------------------------------------------- \n' + str(df[['Letala','Matenda']]) + '\n ' + '------------------------------------------------ \n TSAZ -- tsamba la matenda')
        
        # description of choosen animal disease (chichewa)
        elif (np.any(df6.Letala.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          pld_D = df6.loc[df6['Letala'] == inc,'Kulongosola'].values
          msg = response.message(str(pld_D[0]))
         
        # knowing about zomera
        elif ('knwp' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          output = requests.get(url = "https://1atqmr.deta.dev/zomera_zonse/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message("------TSAMBA LA ZOMERA------- \n --------------------------------------------\n" + str(df[['Letala','Zomera']]) + "\n " + " ------------------------------------------------ \n tsam -- tsamba lalikulu")
        
        # description of the choosen chomera
        elif (np.any(dff9.Letala.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          zomera = dff9.loc[dff9['Letala'] == inc,'Kulongosola'].values
          msg = response.message(str(zomera[0]))  
         
        # knowing about ziweto
        elif ('knwa' in inc) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          output = requests.get(url = "https://1atqmr.deta.dev/ziweto_zonse/")
          df = pd.DataFrame(output.json()['_items'])
          msg = response.message("---------TSAMBA LA ZIWETO---------- \n --------------------------------------------\n" + str(df[['Letala','Ziweto']]) + "\n " + " ------------------------------------------------ \n tsam -- tsamba lalikulu")
        
        # description of the selected chiweto
        elif (np.any(dff10.Letala.values == inc) == True) & (dff3.loc[dff3['user_number'] == phone_number ,'lan'].values[0] == 'chichewa'):
          ziweto = dff10.loc[dff10['Letala'] == inc,'Kulongosola'].values
          msg = response.message(str(ziweto[0]))
          
        elif ("vn" in inc) | ('mx' in inc):
          
          # updating to english_vn if language was in chichewa or eng
          if np.any(dff3.user_number.values == phone_number):
             requests.put(url = 'https://lkdzzx.deta.dev/update_language/',params = {'key':dff3.loc[dff3['user_number'] == phone_number,'key'].values[0],'user_number':phone_number,'lan' : 'english_vn'})  
              
          else:
            # registering a new number in english_vn
            requests.post(url = 'https://lkdzzx.deta.dev/language_change/',params = {'user_number':phone_number,'lan' : 'english_vn'})
            
          msg = response.message('VN MENU')
          msg.media('https://1atqmr.deta.dev/stream/menu.mp4')
        
        else:
          output = 'still in development'
          msg = response.message(output)
    
          
    else:
        if media.startswith('image/'):
            file_url = request.values['MediaUrl0']
            msg = response.message(post_photo(file_url))
            msg.media(file_url)
            
        elif media.startswith('video/'):
            file_url = request.values['MediaUrl0']
            msg = response.message('you sent us this video')
            msg.media(file_url)
            
        else:
            msg = response.message('we dont understand what you have given bro')
          
    return str(response)
 
if __name__ == '__main__':
  app.run()

