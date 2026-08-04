FROM python:3.13.14-slim

ENV PYTHONUNBUFFERED 1

RUN useradd sber_test -d /sber_test -s /sbin/nologin -c "sber_test app user"
RUN mkdir /sber_test
WORKDIR /sber_test
COPY ./app/requirements.txt /tmp/
COPY . .
RUN chown -R sber_test /sber_test/

RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt

USER sber_test

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
