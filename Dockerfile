# syntax=docker/dockerfile:1

#FROM python:3.11.4-bullseye
FROM python:3.11-slim
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-m" , "flaskapp", "run", "--host=0.0.0.0"]
EXPOSE 8080

 