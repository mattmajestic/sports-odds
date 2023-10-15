#!/bin/bash

# Install the required Python packages
pip install -r requirements.txt

# Run the FastAPI application using Uvicorn
uvicorn odds:app --host 0.0.0.0 --port 8885
