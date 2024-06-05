FROM python:3.7.2-stretch

WORKDIR /app

COPY . /app

RUN pip install pipenv

RUN python3 -m pipenv lock --requirements > requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080
CMD [ "uwsgi", "app.ini"]
