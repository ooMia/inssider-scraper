# initialization

```sh
touch README.md
touch .gitignore
touch pyproject.toml
```

# development

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
inssider --url https://example.com/abc/1
```
