from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import pandas as pd
import numpy as np
import sklearn



app = Flask(__name__)
X = pd.read_csv("Data/X.csv")
X = X.drop('Unnamed: 0', axis=1)
model = pickle.load(open('Model/price_car_predictor_brands.pickle', 'rb'))
scaler = pickle.load(open('Model/scaler_train.pickle', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict(years_old=4, km=20000, doors=5, location="Madrid", brand="Audi", horse_power=125, gear=0, seller=0, fuel=1, description_len=548):

    if request.method == 'POST':
        years_old = int(request.form['Years_Old'])
        km=int(request.form['Kms_Driven'])
        doors=int(request.form['Doors'])#
        horse_power =float(request.form['Horse_Power'])
        description_len=int(request.form['Length_Add'])


        fuel=request.form['Fuel_Type_Petrol']

        if(fuel=='Petrol'):
               fuel=0
        else:
               fuel=1

        seller=request.form['Seller_Type_Individual']
        if(seller=='Individual'):
            seller=0
        else:
            seller=1

        gear=request.form['Transmission_Mannual']
        if(gear=='Mannual'):
            gear=0
        else:
            gear=1
        
        location=request.form['Location']
        location = location.lower()

        brand=request.form['Car_Brand']
        brand = brand.capitalize()

        x= np.zeros(len(X.columns))
        x[0] = horse_power
        x[1] = years_old
        x[2] = km
        x[3] = doors
        x[4] = description_len
        x[5] = gear
        x[6] = seller
        x[7] = fuel

        try: 
            loc_index = np.where(X.columns==location)[0][0] 
        # we use np.where method to loc the index for the location
        
            if loc_index >= 0:
                x[loc_index] = 1
 
        except IndexError:
            pass
    
        try: 
            loc_index2 = np.where(X.columns==brand)[0][0] 
        # X is an np array so we use where method to locate the index 

            if loc_index2 >= 0:
                x[loc_index2] = 1
            
        except IndexError:
            pass
    
        x1 = scaler.transform(x[:5].reshape(-1, 1).T) 
        # Rescaling non dummy variables
        x2 = x[5:].reshape(-1, 1).T 
        # Dummy variables not rescaled
        x = np.concatenate((x1, x2), axis=1)

        prediction=model.predict(x)[0]

        output=round(prediction,1)

        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="The estimated value for this second hard car is {} euros".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
