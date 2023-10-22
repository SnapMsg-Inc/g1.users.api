FROM python:3.11.5 as base

WORKDIR /usr/snapmsg-users

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .


# test stage
#FROM base as test
#RUN pip install pytest httpx
#CMD pytest


# production stage
#FROM base as prod
EXPOSE 3000
#ENV DD_SERVICE=users-ms
#ENV DD_LOGS_INJECTION=true
#ENV DD_ENV=prod

#CMD ["uvicorn", "src.main:app" ,"--host", "0.0.0.0", "--port", "3000"] 
CMD ["ddtrace-run", "uvicorn", "src.main:app" ,"--host", "0.0.0.0", "--port", "3000"] 
#ENV NEW_RELIC_CONFIG_FILE=/usr/snapmsg-users/newrelic.ini

