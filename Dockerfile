FROM python:3.7-alpine

WORKDIR /opt/app/

COPY dist/termlink-*.tar.gz .

RUN mkdir termlink
RUN tar zxf termlink-*.tar.gz -C /opt/app/termlink --strip-components 1

RUN pip install --quiet --upgrade pip
RUN pip install /opt/app/termlink-*.tar.gz
RUN rm termlink-*.tar.gz

ENTRYPOINT [ "python", "-m", "termlink" ]
