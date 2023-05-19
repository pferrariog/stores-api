
# MarketPlace API

Created to simulate an marketplace where an user can register yourself and your stores w/ their own products based on department tags

## Requirements

- Python 3.10+
- Poetry 1.3+
- Docker 23.0+ (Optional)

## Usage

- Create configuration files

  > - This project uses [Dynaconf](https://www.dynaconf.com/flask/) as management tool/library, so checkout their documentation for more details

  - settings.toml - Here goes project configuration
  - .secrets.toml - Here goes enviroment secrets
  - .env - Here goes your flask configurations

- Create and activate virtual env + install requirements from pyproject.toml

```sh
    poetry shell
    poetry install
```

- Make database migration

```sh
    flask db init  # just on first time
    flask db migrate
    flask db upgrade  # set latest version
```

- Run flask app after setting the app path in a .env file

```sh
    flask run
```

- If running with Docker, just run the commands below

```sh
    docker build -t $IMAGE_NAME .
    docker run -d -p 80:80 --name $CONTAINER_NAME $IMAGE_NAME
```

## TODO

- Add admin statement to JWT Claims
- Set blocklist on redis
- Update readme and contributing file
