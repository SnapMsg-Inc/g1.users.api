FROM python:3.9

WORKDIR /usr/snapmsg-users

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000

ENV NEW_RELIC_CONFIG_FILE=/usr/snapmsg-users/newrelic.ini

#CMD ["newrelic-admin", "run-program", "uvicorn", "src.main:app" ,"--host", "0.0.0.0", "--port", "3000"] 
CMD ["uvicorn", "src.main:app" ,"--host", "0.0.0.0", "--port", "3000"] 
