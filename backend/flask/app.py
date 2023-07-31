import multiprocessing
from redfin_scraper import RedfinScraper
import pandas as pd
import numpy as np
import requests
import json
import pickle
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import mean_absolute_percentage_error
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from secret import BRIDGE_KEY

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
@app.route("/", methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def profit_retriver():
    city_states = []
    zip_codes = []
    city_states.append(request.headers.get('location'))
    scraper = RedfinScraper()
    zip_database_path = "/Users/pradnyankhodke/Projects/VSCProjects/House Flip Web App/HouseFlipper/backend/zip_code_database.csv"
    location = str.split(city_states[0], sep=',')
    zip_db = pd.read_csv(zip_database_path)
    zip_codes.append(zip_db.loc[((zip_db['primary_city'] == location[0]) & (zip_db['state'] == location[1].strip()))]['zip'])
    zip_codes = list(zip_codes[0])
    main_db = pd.DataFrame(columns=['PROPERTY TYPE','BEDS', 'BATHS', 'SQUARE FEET', 'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET'])
    scraper.setup("/Users/pradnyankhodke/Projects/VSCProjects/House Flip Web App/HouseFlipper/backend/zip_code_database.csv", multiprocessing=False)
    scraper.scrape(city_states=city_states, zip_codes=zip_codes)
    data = scraper.get_data("D001")
    data = data.drop(['SOLD DATE'], axis=1)
    data.insert(len(data.iloc[0]), 'ZESTIMATE', 0)
    data.insert(len(data.iloc[0]), 'PREDICTED PRICE', 0)
    nonnull_data = data[['ADDRESS', 'PROPERTY TYPE', 'BEDS', 'BATHS', 'SQUARE FEET', 'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET']]
    nonnull_data = nonnull_data.dropna()
    model_data = nonnull_data[['PROPERTY TYPE', 'BEDS', 'BATHS', 'SQUARE FEET', 'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET']]
    main_db = pd.concat([main_db, model_data], axis=0)

    s = (main_db.dtypes == 'object')
    object_cols = list(s[s].index)

    OH_encoder = OneHotEncoder(sparse=False)
    OH_cols = pd.DataFrame(OH_encoder.fit_transform(main_db[object_cols]))
    OH_cols.index = main_db.index
    OH_cols.columns = OH_encoder.get_feature_names_out()
    df_final = main_db.drop(object_cols, axis=1)
    df_final = pd.concat([df_final, OH_cols], axis=1)

    columns = ['BEDS', 'BATHS', 'SQUARE FEET', 'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET', 'PROPERTY TYPE_Condo/Co-op', 'PROPERTY TYPE_Mobile/Manufactured Home', 'PROPERTY TYPE_Multi-Family (2-4 Unit)', 'PROPERTY TYPE_Multi-Family (5+ Unit)', 'PROPERTY TYPE_Other', 'PROPERTY TYPE_Ranch', 'PROPERTY TYPE_Single Family Residential', 'PROPERTY TYPE_Townhouse', 'PROPERTY TYPE_Unknown', 'PROPERTY TYPE_Vacant Land']
    for i in range(0, len(columns)):
        if(columns[i] not in df_final.columns):
            df_final.insert(len(df_final.iloc[0]), columns[i], 0)

    # load
    with open('model.pkl', 'rb') as f:
        model_SVR = pickle.load(f)

    cols_when_model_builds = columns
    # print(cols_when_model_builds)
    df_final = df_final[cols_when_model_builds]
    model_prediction = model_SVR.predict(df_final)

    BASE_URL = 'https://api.bridgedataoutput.com/api/v2'
    query_params = {
        "access_token": BRIDGE_KEY,
        "state": "", 
        "city": "",
        "address": ""
    }

    for i in range(0, len(data)):
        query_params["city"] = data.iloc[i]['CITY']
        query_params["state"] = data.iloc[i]['STATE OR PROVINCE']
        query_params["address"] = data.iloc[i]['ADDRESS']
        try:
            zestimate = requests.get(f"{BASE_URL}/zestimates_v2/zestimates", params=query_params).json()['bundle'][0]['zestimate']
            data.loc[i, 'ZESTIMATE'] = zestimate
        except Exception as e:
            print(e)
    
    index = 0
    for ind in nonnull_data.index:
        data.loc[ind, 'PREDICTED PRICE'] = model_prediction[index]
        index += 1 
    
    data.rename(columns={'URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)': "URL"}, inplace=True)
    data = data[['PROPERTY TYPE', 'ADDRESS', 'CITY', 'STATE OR PROVINCE', 'ZIP OR POSTAL CODE', 'PRICE', 'BEDS', 'BATHS', 'LOCATION', 'SQUARE FEET', 'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET', '$/SQUARE FEET', 'HOA/MONTH', 'URL', 'ZESTIMATE', 'PREDICTED PRICE']]
    data.insert(len(data.iloc[0]), 'POTENTIAL PROFIT', 0)

    for i in range(0, len(data)):
        zestimate = data.loc[i, 'ZESTIMATE']
        predicted_price = data.loc[i, 'PREDICTED PRICE']
        price = data.loc[i, 'PRICE']
        data.loc[i, 'POTENTIAL PROFIT'] = max(predicted_price - price, zestimate - price)

    result = data.to_json(orient='records')
    parsed = json.loads(result)
    return json.dumps(parsed, indent=4)

    #data.to_csv('VHDATA.csv')
