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

inssider -h
inssider install -h
inssider test -h
inssider serve -h
```

# ToDo

- [ ] Upload user profile to AWS S3
