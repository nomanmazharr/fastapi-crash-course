from fastapi import FastAPI, HTTPException, Path, Query
import json

app = FastAPI()

def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
data = load_data('data.json')


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

