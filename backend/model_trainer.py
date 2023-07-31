import multiprocessing
from redfin_scraper import RedfinScraper
import pandas as pd
import numpy as np
import requests
import json
import pickle
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LinearRegression
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor
from secret import BRIDGE_KEY

scraper = RedfinScraper()
zip_database_path = "/Users/pradnyankhodke/Projects/VSCProjects/House Flip Web App/HouseFlipper/backend/zip_code_database.csv"
city_states = ["Vernon Hills, IL"]
zip_codes = []
# location = str.split(city_states[0], sep=',')
zip_db = pd.read_csv(zip_database_path)
# zip_codes.append(zip_db.loc[((zip_db['primary_city'] == location[0]) & (zip_db['state'] == location[1].strip()))]['zip'])
# zip_codes = list(zip_codes[0])
main_db = pd.DataFrame(columns=['PROPERTY TYPE','BEDS', 'BATHS', 'SQUARE FEET', 'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET', 'PRICE'])
scraper.setup("/Users/pradnyankhodke/Projects/VSCProjects/House Flip Web App/HouseFlipper/backend/zip_code_database.csv", multiprocessing=False)
# scraper.scrape(city_states=city_states, zip_codes=zip_codes)

start = 16000
end = 18000

# for i in range(1, 5):
#     zip_codes.clear()
#     for j in range(start, end):
#         zip_codes.append(zip_db.loc[j, 'zip'])
#     scraper.scrape(city_states=city_states, zip_codes=zip_codes)
#     start += 2000
#     end += 2000

# for i in range(1, 5):
#     try:
#         data = scraper.get_data(f"D00{i}")
#         data = data[['PROPERTY TYPE','BEDS', 'BATHS', 'SQUARE FEET', 'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET', 'PRICE']]
#         main_db = pd.concat([main_db, data], axis=0)
#     except Exception as e:
#         print(e)
# main_db.to_csv('Training_Dataset.csv', index=False)
main_db = pd.read_csv('Training_Dataset.csv')
# data = scraper.get_data("D001")
# print(len(data))
# data = data.drop(['SOLD DATE'], axis=1)
# print(data.iloc[0])
# data.insert(len(data.iloc[0]), 'ZESTIMATE', 0)
# data.insert(len(data.iloc[0]), 'PREDICTED PRICE', 0)
# nonnull_data = data[['ADDRESS', 'PROPERTY TYPE', 'BEDS', 'BATHS', 'SQUARE FEET', 'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET']]
# nonnull_data = nonnull_data.dropna()
# model_data = nonnull_data[['PROPERTY TYPE', 'BEDS', 'BATHS', 'SQUARE FEET', 'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET']]
# main_db = pd.concat([main_db, model_data], axis=0)
# print(main_db)

# BASE_URL = 'https://api.bridgedataoutput.com/api/v2'
# response = []
# zillow_not_found = []
# query_params = {
#     "access_token": '98bd3a1daa4fa46e4151416dff50b3d1',
#     "address.city": "", 
#     "address.state": "",
#     "address.street": ""
# }

# for i in range(0, len(data)):
#     query_params["address.city"] = data.iloc[i]['CITY']
#     query_params["address.state"] = data.iloc[i]['STATE OR PROVINCE']
#     query_params["address.full"] = data.iloc[i]['ADDRESS']
#     try:
#         json = requests.get(f"{BASE_URL}/pub/parcels", params=query_params).json()['bundle'][0]
#         response.append(query_params)
#     except Exception as e:
#         zillow_not_found.append(query_params)
    
# with open('VHData.json', 'w') as out_file:
#      json.dump(response, out_file, sort_keys = True, indent = 4, ensure_ascii = False)


#house_details = json.loads("VHData.json")



#will need to find dataset that will contain the common characteristics that all the houses have. Most likely can just scraped values like beds, baths, sqft, lotsize, ear byult, days on market, and $/sqft.
#can also add column for zestimate and use that to predict sale price
#the thing is will need to create a massive dataset for thaat can prob just check zillow or redfin
#can then use that to train, and will just have to pass in those same inputs everytime. 
#plan can be then to push actual sale price subtracted by predicted sale price and show how much real value/profit there is
#can sort by profit and then just display on frontend


# training model
# dataset = pd.read_excel("HousePricePrediction.xlsx")
# dataset.drop(['Id'], axis=1, inplace=True)
# dataset['SalePrice'] = dataset['SalePrice'].fillna(dataset['SalePrice'].mean())
# new_dataset = dataset.dropna()
# new_dataset.isnull().sum()

main_db['PRICE'] = main_db['PRICE'].fillna(main_db['PRICE'].mean())
main_db = main_db.dropna()
main_db.isnull().sum()

s = (main_db.dtypes == 'object')
object_cols = list(s[s].index)

OH_encoder = OneHotEncoder(sparse_output=False)
OH_cols = pd.DataFrame(OH_encoder.fit_transform(main_db[object_cols]))
OH_cols.index = main_db.index
OH_cols.columns = OH_encoder.get_feature_names_out()
df_final = main_db.drop(object_cols, axis=1)
df_final = pd.concat([df_final, OH_cols], axis=1)
print(len(df_final))
# columns = ['BEDS', 'BATHS', 'SQUARE FEET', 'LOT SIZE', 'YEAR BUILT', 'PROPERTY TYPE_Condo/Co-op', 'PROPERTY TYPE_Mobile/Manufactured Home', 'PROPERTY TYPE_Multi-Family (2-4 Unit)', 'PROPERTY TYPE_Single Family Residential', 'PROPERTY TYPE_Townhouse']
# for i in range(0, len(columns)):
#     if(columns[i] not in df_final.columns):
#         df_final.insert(len(df_final.iloc[0]), columns[i], 0)

X = df_final.drop(['PRICE'], axis=1)
Y = df_final['PRICE']
 
# Split the training set into
# training and validation set
# rbX = RobustScaler()
# rbY = RobustScaler()
# X_std = rbX.fit_transform(X)
# Y_std = rbY.fit_transform(Y)
X_train, X_valid, Y_train, Y_valid = train_test_split(X, Y, train_size=0.80, test_size=0.20, random_state=0)

# model_SVR = svm.SVR()
# model_SVR.fit(X_train,Y_train)
# Y_pred = model_SVR.predict(X_valid)
# # Y_pred = inverse_transform(Y_pred)
# print(Y_pred)
# print(mean_absolute_percentage_error(Y_valid, Y_pred))
# #got 94.62

# model_RFR = RandomForestRegressor(n_estimators=10)
# model_RFR.fit(X_train, Y_train)
# Y_pred = model_RFR.predict(X_valid)
# print(mean_absolute_percentage_error(Y_valid, Y_pred))
# #52.1
# model_LR = LinearRegression()
# model_LR.fit(X_train, Y_train)
# Y_pred = model_LR.predict(X_valid)
# print(mean_absolute_percentage_error(Y_valid, Y_pred))
#4840
cb_model = CatBoostRegressor()
cb_model.fit(X_train, Y_train)
preds = cb_model.predict(X_valid)
cb_r2_score=r2_score(Y_valid, preds)
print(cb_r2_score)
#.425
# save
with open('model.pkl','wb') as f:
    pickle.dump(cb_model,f)

# load
# with open('model.pkl', 'rb') as f:
#     model_SVR = pickle.load(f)

# cols_when_model_builds = columns
# # print(cols_when_model_builds)
# df_final = df_final[cols_when_model_builds]
# model_prediction = model_SVR.predict(df_final)

# BASE_URL = 'https://api.bridgedataoutput.com/api/v2'
# query_params = {
#     "access_token": BRIDGE_KEY,
#     "state": "", 
#     "city": "",
#     "address": ""
# }

# for i in range(0, len(data)):
#     query_params["city"] = data.iloc[i]['CITY']
#     query_params["state"] = data.iloc[i]['STATE OR PROVINCE']
#     query_params["address"] = data.iloc[i]['ADDRESS']
#     try:
#         zestimate = requests.get(f"{BASE_URL}/zestimates_v2/zestimates", params=query_params).json()['bundle'][0]['zestimate']
#         print(zestimate)
#         data.loc[i, 'ZESTIMATE'] = zestimate
#     except Exception as e:
#         print(e)

# print(model_prediction)
# print(nonnull_data)
# index = 0
# for ind in nonnull_data.index:
#     data.loc[ind, 'PREDICTED PRICE'] = model_prediction[index]
#     index += 1 

# data.rename(columns={'URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)': "URL"}, inplace=True)
# data = data[['PROPERTY TYPE', 'ADDRESS', 'CITY', 'STATE OR PROVINCE', 'ZIP OR POSTAL CODE', 'PRICE', 'BEDS', 'BATHS', 'LOCATION', 'SQUARE FEET', 'LOT SIZE', 'YEAR BUILT', 'DAYS ON MARKET', '$/SQUARE FEET', 'HOA/MONTH', 'URL', 'ZESTIMATE', 'PREDICTED PRICE']]

# #data.to_csv('VHDATA.csv')

# result = data.to_json(orient='records')
# parsed = json.loads(result)
# json = json.dumps(parsed, indent=4)
# print(json)