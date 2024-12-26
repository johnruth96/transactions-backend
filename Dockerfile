FROM python:3.13-bullseye

RUN pip install poetry==1.8.5

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry export --with=prod -o requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "transactions.wsgi"]