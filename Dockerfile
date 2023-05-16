FROM python:3.11.3

# RUN apt-get update -y && apt-get install -y python3-pip python3-dev

WORKDIR /app

COPY . .

RUN pip install poetry==1.4.0

RUN poetry install --no-dev

EXPOSE 5000

ENTRYPOINT ["poetry", "run"]

CMD ["flask", "run", "--host", "0.0.0.0"]
