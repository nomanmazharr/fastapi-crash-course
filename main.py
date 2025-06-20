from fastapi import FastAPI, HTTPException, Path, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
from fastapi.responses import JSONResponse

app = FastAPI()

def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
data = load_data('data.json')

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

class Patient(BaseModel):
    patient_id: Annotated[str, Field(..., description='Should be unique to identify patients', example='P001')]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="city where patient lives")]
    age: Annotated[int, Field(..., description="Age of the patient", gt=0, le=100)]
    gender: Annotated[Literal['male', 'female'], Field(..., description='gender of the patient')]
    height: Annotated[float, Field(..., description='Height of the patient')]
    weight: Annotated[float, Field(..., description="Weight of the patient")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round((self.weight)/((self.height)**2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Under-weight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Obese"
        else:
            return "Severe Obesity"

class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    city: Annotated[Optional[str], Field(default=None)]
    gender: Annotated[Literal['male', 'female'], Field(default='male')]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


@app.get('/')
def home():
    return 'Welcome to Patient Management System'


@app.get('/about')
def about():
    return "this is about page of our app"

@app.get('/view')
def get_records():
    return data

@app.get('/patient/{patient_id}')
def get_patient(patient_id: str = Path(..., description="ID of the patient", example="001")):

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_records(sort_by: str = Query(..., desciption="sort by age and bmi"), order: str = Query('asc', description="sort in ascending or descending order")):
    if sort_by not in ['age', 'bmi']:
        raise HTTPException(status_code=400, detail="invalid selection, select between age or bmi")

    if order not in ['asc', 'dsc']:
        raise HTTPException(status_code=400, detail="invalid selection, select between asc or dsc")

    sort_order = True if order == 'dsc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def new_patient(patient: Patient):
    if patient.patient_id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.patient_id] = patient.model_dump(exclude='id')

    save_data(data)

    return JSONResponse(status_code=201, content=f"patient {patient.patient_id} created successfully")

@app.put('/edit/{patient_id}')
def updatepatient(patient_id: str, patient_update: UpdatePatient):
    if patient_id not in data:
        raise HTTPException(status_code=400, detail=f'patient {patient_id} not found')

    patient_info =   data[patient_id]
    updated_patient = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient.items():
        patient_info[key] = value

    patient_info['patient_id'] = patient_id

    patient_pydantic_object = Patient(**patient_info)

    patient_info = patient_pydantic_object.model_dump(exclude='id')
    data[patient_id] = patient_info

    save_data(data)

    return JSONResponse(status_code=201, content=f"patient {patient_id} updated successfully")

@app.delete('/del-patient')
def dlt_patient(patient_id: str):
    if patient_id not in data:
        return HTTPException(status_code=400, detail=f"Patient {patient_id} not found")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=201, content=f"Patient {patient_id} deleted successfully")
# print(data)