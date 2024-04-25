FROM python:3.10-buster

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry install

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1843", "--workers", "1"]