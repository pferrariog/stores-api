FROM python:3.11.3

WORKDIR /app

COPY . .

RUN pip install poetry==1.4.0

RUN poetry install --without dev --no-cache --no-interaction

ENV FLASK_APP=stores/app.py

ENTRYPOINT ["poetry", "run"]

CMD ["gunicorn", "-b", "0.0.0.0:80", "stores.app:create_app()"]
