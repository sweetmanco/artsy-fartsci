FROM python:3.10.6-buster
COPY artsyfartsci /artsyfartsci
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install typing-extensions --upgrade
CMD uvicorn artsyfartsci.api.fast:app --host 0.0.0.0 --port $PORT
