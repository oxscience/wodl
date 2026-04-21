FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY requirements.txt pyproject.toml ./
COPY wodl/ ./wodl/
COPY examples/ ./examples/
COPY static/ ./static/
COPY playground.py ./

RUN pip install -r requirements.txt && pip install -e .

EXPOSE 5051

CMD gunicorn --bind 0.0.0.0:${PORT:-5051} --workers 2 --timeout 30 playground:app
