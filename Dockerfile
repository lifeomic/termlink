FROM python:3.7-alpine

WORKDIR /opt/app/

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY dist/termlink-*.tar.gz .
RUN tar zxf termlink-*.tar.gz -C /opt/app/ --strip-components 1 && rm termlink-*.tar.gz

ENTRYPOINT [ "python", "-m", "termlink" ]