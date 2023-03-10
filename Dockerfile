FROM python:3.10.7

RUN python -m pip install --upgrade pip

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app

COPY . .







