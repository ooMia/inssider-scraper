# initialization

```sh
touch README.md
touch .gitignore
touch pyproject.toml
pip install -e ".[dev]"

docker compose up -d
```

# development

```sh
python3 -m venv .venv
source .venv/bin/activate

inssider install
inssider test
inssider serve
inssider serve --port 8080
```
