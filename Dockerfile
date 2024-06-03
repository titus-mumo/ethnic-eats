FROM python:3.10

WORKDIR /ethnic_eats

COPY requirements.txt /ethnic_eats/
RUN pip install -r requirements.txt

