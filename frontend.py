import streamlit as st
import requests

API_URL = 'http://127.0.0.1:8000/predict'


st.title('Diabetes Predictor')
st.markdown('Enter your details below')

Pregnancies = st.number_input('Pregnancies')
Glucose = st.number_input('Glucose')
BloodPressure = st.number_input("BloodPressure")
SkinThickness = st.number_input("SkinThickness")
Insulin = st.number_input('Insulin')
BMI = st.number_input('bmi')
DiabetesPedigreeFunction = st.number_input('DIabetesPedigreeFunction')
Age = st.number_input('age', min_value=1,max_value=120)

if st.button('Predict'):
    user_input = {
        'Pregnancies': Pregnancies,
        'Glucose': Glucose,
        'BloodPressure': BloodPressure,
        'SkinThickness': SkinThickness,
        'Insulin': Insulin,
        'BMI': BMI,
        'DiabetesPedigreeFunction': DiabetesPedigreeFunction,
        'Age': Age
    }

    try:
        response = requests.post(API_URL, json=user_input)
        result = response.json()
        st.write(result)
        result = result['predicted_category']
        if result ==0:
            st.write('Patient does not have diabetes')
        else:
            st.write('Patient has diabetes')

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to api")