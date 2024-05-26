FROM python:3.12-slim as runtime

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ENV PYTHONPATH=app

WORKDIR /application

COPY run.py .
COPY app app

ENTRYPOINT uvicorn run:app --proxy-headers --host 0.0.0.0 --port 8000

FROM runtime as tests

COPY requirements-tests.txt /tmp/requirements-tests.txt
RUN pip install -r /tmp/requirements-tests.txt

ENV DATABASE_URL=sqlite:///./tests/testdb.db

COPY tests tests

ENTRYPOINT pytest tests
