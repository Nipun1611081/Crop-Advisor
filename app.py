import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd 
 
app = Flask(__name__)
model = pickle.load(open('decision_tree.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():


    '''
    For rendering results on HTML GUI
    '''
    balance_data = pd.read_csv("test.csv")
    df=balance_data[['CROP', 'REGION', 'SOWING_TIME', 'Average Soil_pH','SOIL_TYPE']].copy()
    print(df.head(20))
    df.shape

    #CROP 

    save_crop=df["CROP"].unique()
    crop_dict={}
    count=1
    for i in save_crop:
      crop_dict[i]=count
      count=count+1

    def get_key(val):
        for key, value in crop_dict.items(): 
         if val == value: 
             return key
        return "key doesn't exist"  
  
    

    #REGION 
    save_region=df["REGION"].unique()
    region_dict={}
    count=1
    for i in save_region:
      region_dict[i]=count
      count=count+1

    #SOWING TIME 

    save_sowing=df["SOWING_TIME"].unique()
    sowing_dict={}
    count=1
    for i in save_sowing:
      sowing_dict[i]=count
      count=count+1


    #SOIL TYPE

    save_soil=df["SOIL_TYPE"].unique()
    soil_dict={}
    count=1
    for i in save_soil:
      soil_dict[i]=count
      count=count+1

    month= request.form["month"]
    region= request.form["region"]
    soil= request.form["soil"]
    ph= request.form["ph"]
    region= int(region_dict[region])
    month= int(sowing_dict[month])
    soil= int(soil_dict[soil])
    prediction = model.predict([[region,month,ph,soil]])
    print (model.predict([[region,month,ph,soil]]))
    
    output = (prediction[0])

    return render_template('index.html', prediction_text='Optimum crop should be {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)