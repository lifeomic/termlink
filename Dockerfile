FROM python:3.7-alpine

WORKDIR /opt/app/

COPY dist/termlink-*.tar.gz .

RUN mkdir termlink
RUN tar zxf termlink-*.tar.gz -C /opt/app/termlink --strip-components 1
RUN rm termlink-*.tar.gz

RUN pip install --quiet --upgrade pip
RUN pip install --quiet termlink

ENTRYPOINT [ "python", "-m", "termlink" ]
