FROM python:3.10

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

#CMD uvicorn main:app --host "127.0.0.1" --port "5000"
CMD gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind="0.0.0.0:8000"
