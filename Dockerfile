FROM python:3.9

WORKDIR /usr/src

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["NEW_RELIC_CONFIG_FILE=/usr/src/newrelic.ini newrelic-admin run-program", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000"] 
