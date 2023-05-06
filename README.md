# FastAPI Auth
Clear project with auth model

## .env
Create `.env` file
- DB_URL - str, url for db. For example, `sqlite:///db.db`
- POSTGRES_USER - str
- POSTGRES_PASSWORD - str

Create `db/.env` file
- POSTGRES_USER - str
- POSTGRES_PASSWORD - str

## Test
1. `python -m pytest --cov="."`

## Local Run
1. `pip install -r requirements.txt`
2. `alembic upgrade head`
3. `python main.py`

## Docker-compose
1. `docker-compose up --build`
2. `docker-compose exec web alembic upgrade head`