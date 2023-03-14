FROM python:3.10.7

#RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app

RUN pip install --upgrade pip
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

ADD ./codeforces_app /app/codeforces_app
ADD ./app /app
#ADD ./docker /app/docker

# RUN chmod +x /app/codeforces_app/server-entrypoint.sh
# RUN chmod +x /app/docker/backend/worker-entrypoint.sh

COPY . .
