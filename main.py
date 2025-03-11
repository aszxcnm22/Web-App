from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import numpy as np
import pandas as pd

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

inputWeight = pd.read_csv('./Data/inputWeightInference.csv', header=None).values
outputWeight = pd.read_csv('./Data/outputWeightInference.csv', header=None).values
bias = pd.read_csv('./Data/biasInference.csv', header=None).values

def maxtwoind_mammo(x):
    y = []
    for i in range(x.shape[0]):
        n = np.argmax(x[i, :]) 
        if n == 0:
            y.append([1, 0])
        elif n == 1:
            y.append([0, 1])
        else:
            print("error")
            break
    return np.array(y)

def maxtwoindclass_mammo(x):
    y = []
    for i in range(x.shape[0]):
        n = x[i, :]
        if np.array_equal(n, [1, 0]):
            y.append(1)
        elif np.array_equal(n, [0, 1]):
            y.append(2)
        else:
            print("Error: Invalid prediction")
            y.append(0) 
    return np.array(y)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/introduction", response_class=HTMLResponse)
async def introduction(request: Request):
    return templates.TemplateResponse("introduction.html", {"request": request})

@app.get("/prediction", response_class=HTMLResponse)
async def prediction(request: Request):
    return templates.TemplateResponse("prediction.html", {"request": request})

@app.post("/predict/")
async def predict(data: dict):
    input_values = data["input_values"]
    X_new = np.array([input_values])

    H_new = 1 / (1 + np.exp(-(X_new @ inputWeight + np.tile(bias, (X_new.shape[0], 1)))))
    outputNew = np.dot(H_new, outputWeight)

    yNew = maxtwoind_mammo(outputNew)
    predictionsNew = maxtwoindclass_mammo(yNew)
    confidence = np.max(outputNew)
    if predictionsNew.size > 0:
        prediction = predictionsNew[0] 
    else:
        prediction = 0  

    if prediction == 2:
        result = "Yes Osteoporosis 🦴"
    elif prediction == 1:
        result = "No Osteoporosis 💀"
    else:
        result = "Error in Prediction"
    
    return {"prediction": result, "confidence": confidence * 100}
