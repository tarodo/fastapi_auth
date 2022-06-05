# FastAPI Auth
Clear project with auth model

## .env
Create `.env` file
- DB_URL - str, url for db. For example, `sqlite:///db.db`

## Test
1. `python -m pytest --cov="."`

## Run
1. `pip install -r requirements.txt`
2. `alembic upgrade head`
3. `python main.py`
