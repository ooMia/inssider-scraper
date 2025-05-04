# initialization

```sh
touch README.md
touch .gitignore
touch pyproject.toml

docker compose up -d
```

# development

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
inssider --url https://example.com/abc/1
pytest
uvicorn temp.serve:app --reload
# GET http://localhost:8000/docs
# GET http://localhost:8000/redoc
```
