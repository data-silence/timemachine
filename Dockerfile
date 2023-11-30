FROM python:3.11


WORKDIR /app

COPY . ./
COPY models/ /app/models/
COPY graphs/ /app/graphs/
COPY imports/ /app/imports/
COPY scripts/ /app/scripts/



RUN python -m pip install --upgrade pip && pip install -r requirements.txt


LABEL authors="enjoy@data-silence.com"
LABEL app_name='timemachine'

ENTRYPOINT ["python3", "app.py"]