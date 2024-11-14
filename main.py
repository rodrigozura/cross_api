import os
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

class APIURL(BaseModel):
    api_url: str

API_KEY = os.getenv('API_KEY')

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Cross API"}

@app.post("/external/api")
async def external_api(data: APIURL, status_code=status.HTTP_200_OK):
    print(data)
    headers = { 'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
              }
    
    try:
        response = requests.get(data.api_url, headers=headers)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        return {"error": f"Error: {e}"}
    
    return data

