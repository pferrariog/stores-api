
# MarketPlace API

Created to simulate an marketplace where an user can register yourself and your stores w/ their own products based on department tags

## Requirements

- Python 3.10+
- Poetry 1.3+

## Usage

- Create and activate virtual env + install requirements from pyproject.toml

```sh
    poetry shell && install
```

- Run flask app after setting the app path in a .env file

```sh
    flask run
```

## TODO

- Add admin statement to JWT Claims
- Set blocklist on redis
