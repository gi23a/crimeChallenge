import streamlit as st
import pandas as pd
from goe import map_build  
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import calendar
import plotly.express as px
import joblib
from pdfManager import assign_pdf_data
import json
import re
import os
import boto3
import joblib
import json

#s3
#s3 = boto3.client('s3')
#bucket_name = 'rihal'

model_files = ['RandomForest_model.pkl', 'tfidf_vectorizer.pkl', 'category_dict.json']

model_dir = './model/'  


model = joblib.load(os.path.join(model_dir, 'RandomForest_model.pkl'))
vectorizer = joblib.load(os.path.join(model_dir, 'tfidf_vectorizer.pkl'))

with open(os.path.join(model_dir, 'category_dict.json'), 'r') as file:
    categoryDict = json.load(file)

print("Models loaded successfully.")
print(categoryDict) 
severityDic = {
    "NON-CRIMINAL": "Severity 1",
    "SUSPICIOUS OCC": "Severity 1", #SUSPICIOUS OCCURRENCE to SUSPICIOUS OCC
    "MISSING PERSON": "Severity 1",
    "RUNAWAY": "Severity 1",
    "RECOVERED VEHICLE": "Severity 1",
    "WARRANTS": "Severity 2",
    "OTHER OFFENSES": "Severity 2",
    "VANDALISM": "Severity 2",
    "TRESPASS": "Severity 2",
    "DISORDERLY CONDUCT": "Severity 2",
    "BAD CHECKS": "Severity 2",
    "LARCENY/THEFT": "Severity 3",
    "VEHICLE THEFT": "Severity 3",
    "FORGERY/COUNTERFEITING": "Severity 3",
    "DRUG/NARCOTIC": "Severity 3",
    "STOLEN PROPERTY": "Severity 3",
    "FRAUD": "Severity 3",
    "BRIBERY": "Severity 3",
    "EMBEZZLEMENT": "Severity 3",
    "ROBBERY": "Severity 4",
    "WEAPON LAWS": "Severity 4",
    "BURGLARY": "Severity 4",
    "EXTORTION": "Severity 4",
    "KIDNAPPING": "Severity 5",
    "ARSON": "Severity 5"
}
st.title("PDF Crime Report Extraction")





def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s'-]", '', text) 
    return text.strip()



def predict_pdf(path):

    pdfdata = assign_pdf_data(path) 
    #clean text
    pretext = clean_text(pdfdata["Descript"])
    print(pretext)
    vectext = vectorizer.transform([pretext])
    print(vectext)
    predictCategory = model.predict(vectext)
    print(predictCategory)


    category_names = {v: k for k, v in categoryDict.items()}
    predictedTXT= category_names[predictCategory[0]]

    pdfdata["Category"] = predictedTXT
    pdfdata["Severity"] = assign_severity(pdfdata["Category"])

    print(pdfdata)
    return pdfdata


#test


def assign_severity(category):
    return severityDic.get(category, "Unk")
