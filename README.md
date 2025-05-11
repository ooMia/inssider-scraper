# initialization

```sh
touch README.md
touch .gitignore
touch pyproject.toml

python3 -m venv .venv
source .venv/bin/activate
```

# development

```sh
docker compose up -d

inssider -h
inssider install
inssider format
inssider test
inssider serve
```

# ToDo

- [ ] Upload user profile to AWS S3
