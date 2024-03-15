FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /auth_service/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py"]

EXPOSE 8000
