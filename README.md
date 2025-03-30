# Project Notes

## CSV Files

The CSV files used in this project have been **manually compressed** into zip files for easier storage and handling. 

Make sure to **extract** the zip files to access the raw CSV data.

## Part B: Web UI
We developed a **Streamlit** web dashboard to display the findings. Users can explore crime trends on the map and view the severity levels of different crimes.

## Running Streamlit
1. Install **Streamlit**, and **Plotly** (for heatmap visualization):
   ```bash
   pip install streamlit plotly

Run the app:

streamlit run app.py

#BOUNS
## Prerequisites

- **Docker**: Install Docker from [docker.com](https://www.docker.com/products/docker-desktop).
- **Google Cloud SDK**: Install the Google Cloud SDK from [cloud.google.com](https://cloud.google.com/sdk/docs/install).

## Getting Started

### To Build and Run the Docker Container Locally:

1. **Build the Docker Image**:
   Run this command in the project directory (where the `Dockerfile` is located):

   ```bash
   docker build -t crime-app:latest .
   docker run -p 8501:8501 crime-app:latest

