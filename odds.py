from fastapi import FastAPI
import requests
from dotenv import load_dotenv
import os
import uvicorn

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

@app.get("/")
async def get_sports():
    api_key = os.getenv('ODDS_API_KEY')
    base_url = "https://api.the-odds-api.com/v4/sports/"
    params = {"apiKey": api_key}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from the Odds API"}

if __name__ == "__odds__":
    uvicorn.run(app, host="0.0.0.0", port=8885)