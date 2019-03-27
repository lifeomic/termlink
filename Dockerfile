FROM python:3.7

COPY requirements.txt /opt/app/
COPY requirements-dev.txt /opt/app/

WORKDIR /opt/app/

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

COPY . /opt/app/

CMD [ "python" ]