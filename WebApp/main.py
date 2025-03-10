from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi import Request
import numpy as np
from sklearn.metrics import confusion_matrix
import pandas as pd

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class InputData(BaseModel):
    input_values: list 

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
            x[i] = 1
        elif np.array_equal(n, [0, 1]):
            x[i] = 2
        else:
            print("Error")
            break
        y.append(x[i])
    return np.array(y)


def MultiClassMetrics_mammo_Train(predictions, labels):
    confmat = confusion_matrix(labels, predictions)
    N = confmat.shape[0]

    Accuracy = np.zeros(N)

    for i in range(N):
        TP = confmat[i, i]
        FN = np.sum(confmat[i, :]) - confmat[i, i]
        FP = np.sum(confmat[:, i]) - confmat[i, i]
        TN = np.sum(confmat) - TP - FP - FN

        Accuracy[i] = (TP + TN) / (TP + TN + FN + FP)

    avg_accuracy = np.mean(Accuracy) * 100

    return avg_accuracy

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict/")
async def predict(data: InputData):
    X_new = np.array(data.input_values)
    
    H_new = 1 / (1 + np.exp(-(X_new @ inputWeight + np.tile(bias, (X_new.shape[0], 1)))))
    outputNew = np.dot(H_new, outputWeight)

    yNew = maxtwoind_mammo(outputNew)
    predictionsNew = maxtwoindclass_mammo(yNew)
    predictionsNew = predictionsNew[1, 1]

    if predictionsNew == 2:
        result = "Yes Osteoporosis 🦴"
    elif predictionsNew == 1:
        result = "No Osteoporosis 💀"
    else:
        result = "Error in Prediction"
    
    return {"prediction": result}
