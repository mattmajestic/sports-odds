from fastapi import FastAPI, Response
from fastapi.openapi.models import Info
from fastapi.openapi.models import ExternalDocumentation
from fastapi.responses import RedirectResponse, HTMLResponse
import requests
from dotenv import load_dotenv
import os
import uvicorn
import numpy as np
import io
import urllib
import base64
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go


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

@app.get("/soccer/epl/chart")
async def get_calcs():
    # Query the other route to get the data
    data = await get_epl_odds()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Group the data by the bookmaker and calculate the average and sum of price differences
    grouped = df.groupby('bookmaker')['price_diff'].agg(['mean', 'sum']).reset_index()

    # Sort the data from highest to lowest average price difference
    grouped = grouped.sort_values('mean', ascending=False)

    # Create a Plotly chart
    fig = go.Figure()

    # Add a bar chart for the average price difference
    fig.add_trace(go.Bar(name='Average', x=grouped['bookmaker'], y=grouped['mean']))

    # Add a line chart for the total price difference with a second y-axis
    fig.add_trace(go.Scatter(name='Total', x=grouped['bookmaker'], y=grouped['sum'], yaxis='y2'))

    # Update the layout to include the second y-axis
    fig.update_layout(
        yaxis2=dict(
            title='Total',
            overlaying='y',
            side='right'
        ),
        barmode='group'
    )

    # Convert the Plotly chart to HTML and return it
    html = fig.to_html(full_html=False)
    return HTMLResponse(content=html)

if __name__ == "__odds__":
    uvicorn.run(app, host="0.0.0.0", port=8885)