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
from modelManager import predict_pdf 
import boto3
import joblib

import os

import boto3
import pandas as pd

#client +downloading files
#s3 = boto3.client('s3')

##bucket_name = 'rihal'


data_files = ['final_data.csv', 'crime_severity_Val.csv']

data_dir = './data/'  
try:
    data = pd.read_csv(os.path.join(data_dir, 'final_data.csv'))
    valdata = pd.read_csv(os.path.join(data_dir, 'crime_severity_Val.csv'))
    print("Data loaded successfully")
except Exception as e:
    print("Error loading data files: ")

#pages 
st.sidebar.title("pages")
page = st.sidebar.radio("Select a page:", ["Home", "PDF Report Calssification"])



def mainPage():
    map_type = st.radio("Choose Map Type:", ["category", "heatmap"])

    map_data_type = st.radio("Select Data for Visualization::", ["Full Dataset", "Validation Set"])

    # Choose the dataset 
    if map_data_type == "Full Dataset":
        selected_data = data
    else:
        selected_data = valdata



    fig = map_build(selected_data, mapType=map_type)


    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Most Common Crimes")
    crime_counts = selected_data['Category'].value_counts().head(5).sort_values(ascending=True) 
    st.bar_chart(crime_counts)



    st.subheader("Crimes by Day of Week")
    day_of_week_counts = selected_data['DayOfWeek'].value_counts().sort_index()
    st.bar_chart(day_of_week_counts)

    st.subheader("Crimes by Hour of Day")
    selected_data['Hour'] = pd.to_datetime(selected_data['Dates']).dt.hour
    hourly_crimes = selected_data['Hour'].value_counts().sort_index()
    st.bar_chart(hourly_crimes)


    #heat map for day and h
    selected_data['DayOfWeek'] = pd.Categorical(selected_data['DayOfWeek'], categories=list(calendar.day_name), ordered=True)
    heatmap_data = selected_data.groupby([selected_data['DayOfWeek'], pd.to_datetime(selected_data['Dates']).dt.hour]).size().unstack(fill_value=0)
    fig = px.imshow(heatmap_data, 
                labels=dict(x="Hour", y="Day of Week", color="Number of Crimes"), 
                title="Crimes by Day and Hour",
                color_continuous_scale="YlOrRd")
    st.plotly_chart(fig, use_container_width=True)


    st.subheader("Crime Severity Distribution")
    severity_counts = selected_data['Assigned_Severity'].value_counts()
    st.bar_chart(severity_counts)






    st.subheader("Crime Prediction for Validation Set")
    st.dataframe(valdata[['Descript', 'Category','Predicted_Category', 'Assigned_Severity']].head(10))


    # Confusion Matrix
    st.subheader("Confusion Matrix for Validation Set")

    category_names = list(valdata['Category'].unique())
    confusion_matrixVal = confusion_matrix(valdata['Category'], valdata['Predicted_Category'])

    #name category 
    namedconfusion_matrixVal = pd.DataFrame(confusion_matrixVal, index=category_names,  columns=category_names)
    plt.figure(figsize=(10, 8))
    sns.heatmap(namedconfusion_matrixVal, annot=True, fmt='d', cmap='Blues', linewidths=0.4, linecolor='black')
    #plt.title('Confusion Matrix for Validation')
    plt.xlabel('Predicted Categories')
    plt.ylabel('Real Categories')
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    st.pyplot(plt)



#navigate

if page == "Home":

    st.title("CityX Crime ")
    mainPage()
    
    

elif page == "PDF Report Calssification":
    st.title("PDF Crime Report Extraction")

    uploaded = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded:
        #reset btn 
        st.session_state.predict_done = False 
        #clear old table when uploding 
        result= {}
        extracted_table = st.table(result)
        extracted_table.empty() 
     
        st.empty()
        pdf_data = assign_pdf_data(uploaded)

        buttonPredict =st.button("Predict crime Category and Severity")
        headert  =st.subheader("Extracted Data:")
        #st.table(pdf_data)
        extracted_table = st.table(pdf_data)
        if buttonPredict and not st.session_state.get("predict_done", False):
         
            extracted_table.empty() 
   
            headert.empty()
            result = predict_pdf(uploaded)  
            st.subheader("Predicted Data:")
            extracted_table =st.table(result)
            st.session_state.predict_done = True


            print("Ddddddd")
            print(result)
            if 'Latitude (Y)' in result and 'Longitude (X)' in result and 'Category' in result and 'Address' in result:
                if isinstance(result, dict):
                    result = [result]

                map_data = pd.DataFrame(result)
               


                map_data.rename(columns={
                    'Latitude (Y)': 'Latitude real (Y)',
                    'Longitude (X)': 'Longitude real (X)'
                }, inplace=True)

                #x , y from str to num
                map_data['Latitude real (Y)'] = pd.to_numeric(map_data['Latitude real (Y)'])
                map_data['Longitude real (X)'] = pd.to_numeric(map_data['Longitude real (X)'])



                fig = map_build(map_data, "single")

         
                st.plotly_chart(fig, use_container_width=True)
        elif st.session_state.get("predict_done", False):
            st.warning("Prediction already Done. Please upload a new PDF to predict again.")

      