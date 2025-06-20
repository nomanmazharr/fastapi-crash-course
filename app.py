from fastapi import FastAPI
from pydantic import BaseModel, Field
import pickle
from typing import Annotated
import pandas as pd
from fastapi.responses import JSONResponse

app = FastAPI()

with open('ml_model/model.pkl', 'rb') as f:
    model = pickle.load(f)

class UserInput(BaseModel):
    Pregnancies: Annotated[int, Field(..., description='Number of times a person has been pregnant (e.g., 0, 3, 5)')]
    Glucose: Annotated[int, Field(..., description='Blood sugar level measured 2 hours after a glucose test (e.g., 85, 140, 200 mg/dL)')]
    BloodPressure: Annotated[int, Field(..., description='Diastolic blood pressure in mm Hg (e.g., 60, 80, 90 mm Hg)')]
    SkinThickness: Annotated[int, Field(..., description='Thickness of the skin fold on the triceps, measured in millimeters (e.g., 15, 25, 35 mm)')]
    Insulin: Annotated[int, Field(..., description='Insulin level in the blood 2 hours after glucose intake, measured in microunits per milliliter (e.g., 15, 80, 200 mu U/ml).')]
    BMI: Annotated[float, Field(..., description='Body Mass Index, calculated as weight (kg) divided by height squared (m²) (e.g., 22.5, 30.1, 35.7)')]
    DiabetesPedigreeFunction: Annotated[float, Field(..., description='A score indicating the likelihood of diabetes based on family history (e.g., 0.1, 0.5, 1.2). 0 means less likelihood 1 mean more likelihoodq')]
    Age: Annotated[int, Field(..., description='Age of the patient')]


@app.get('/')
def home():
    return {'message': 'Welcome to Diabetes Prediction System'}

@app.post('/predict')
def predict(data: UserInput):
    input_df = pd.DataFrame([
        {
            'Pregnancies': data.Pregnancies,
            'Glucose': data.Glucose,
            'BloodPressure': data.BloodPressure,
            'SkinThickness': data.SkinThickness,
            'Insulin': data.Insulin,
            'BMI': data.BMI,
            'DiabetesPedigreeFunction': data.DiabetesPedigreeFunction,
            'Age': data.Age
        }
    ])

    result = model.predict(input_df)[0]
    # return {"prediction": int(result)}
    # return int(result)
    # print(result)

    return JSONResponse(status_code=200, content={'predicted_category': int(result)})