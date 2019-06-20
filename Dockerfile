FROM python:3.7-alpine

WORKDIR /opt/app/

RUN pip install --quiet --upgrade pip

COPY dist/termlink-*.tar.gz .

RUN mkdir termlink \
    && tar zxf termlink-*.tar.gz -C /opt/app/termlink --strip-components 1 \
    && pip install /opt/app/termlink-*.tar.gz \
    && rm termlink-*.tar.gz

ENTRYPOINT [ "python", "-m", "termlink" ]
