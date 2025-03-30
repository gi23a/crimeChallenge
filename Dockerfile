FROM python:3.10-slim

#the app directory
WORKDIR /app

#download requirements.txt
COPY requirements.txt .

# Upgrade pip , setuptools, and wheel before installing requirements

RUN pip install --upgrade pip 
RUN  pip install --no-cache-dir -r requirements.txt

#copy the app to the container 
COPY ./data /app/data
COPY ./model /app/model
COPY ./src /app/src



EXPOSE 8501
CMD ["streamlit", "run", "/app/src/main.py"]
