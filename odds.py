from fastapi import FastAPI
from fastapi.openapi.models import Info
from fastapi.openapi.models import ExternalDocumentation
from fastapi.responses import RedirectResponse
import requests
from dotenv import load_dotenv
import os
import uvicorn

# Load environment variables from the .env file
# load_dotenv()

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

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """
    Redirect to the documentation.
    """
    response = RedirectResponse(url='/docs')
    return response

@app.get("/sports", summary="Get Sports Data")
async def get_sports():
    """
    Retrieve sports data available from the Odds API.
    """
    api_key = os.getenv('ODDS_API_KEY')
    base_url = "https://api.the-odds-api.com/v4/sports/"
    params = {"apiKey": api_key}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from the Odds API"}

@app.get("/soccer/epl/odds")
async def get_epl_odds(
    regions: str = "us"
):
    """
    Returns a list of upcoming and live games with recent odds for the English Premier League, region and market.
    """
    base_url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
    params = {
        "apiKey": os.getenv('ODDS_API_KEY'),
        "regions": regions
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from the Odds API"}

@app.get("/soccer/epl/calcs")
async def get_epl_odds():
    base_url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
    params = {
        "apiKey": os.getenv('ODDS_API_KEY'),
        "regions": "us"
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        return {"error": "Failed to fetch data from the Odds API"}

    data = response.json()

    prices = []
    for item in data:
        for bookmaker in item['bookmakers']:
            for market in bookmaker['markets']:
                if len(market['outcomes']) >= 2:
                    price_diff = abs(market['outcomes'][0]['price'] - market['outcomes'][1]['price'])
                    prices.append({
                        "bookmaker": bookmaker['key'],
                        "team1": market['outcomes'][0]['name'],
                        "price1": market['outcomes'][0]['price'],
                        "team2": market['outcomes'][1]['name'],
                        "price2": market['outcomes'][1]['price'],
                        "price_diff": price_diff
                    })

    return prices

if __name__ == "__odds__":
    uvicorn.run(app, host="0.0.0.0", port=8885)