from fastapi import FastAPI
from fastapi.openapi.models import Info
from fastapi.openapi.models import ExternalDocumentation
import requests
from dotenv import load_dotenv
import os
import uvicorn

# Load environment variables from the .env file
load_dotenv()

app = FastAPI(
    title="Sports Odds API",
    description="An API to retrieve sports odds data.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Sports",
            "description": "Endpoints related to sports data.",
        }
    ],
    info=Info(
        title="Sports Odds API",
        version="1.0.0",
        description="An API to retrieve sports odds data.",
        terms_of_service="https://sports-odds.onrender.com/terms",
        contact={
            "name": "Matt Majestic",
            "url": "https://www.youtube.com/@majesticcoding",
        },
        license={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0",
        },
    ),
    external_docs=ExternalDocumentation(
        description="Find more information here",
        url="https://sports-odds.onrender.com/docs",
    ),
)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8885)
