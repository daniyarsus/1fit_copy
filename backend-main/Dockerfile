FROM python:3.10

RUN mkdir /backend_app

WORKDIR /backend_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


RUN chmod a+x docker/*.sh





