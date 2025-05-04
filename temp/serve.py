import tomllib
from pathlib import Path

from fastapi import FastAPI


def get_project_version() -> str:
    try:
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            pyproject_data = tomllib.load(f)
            return pyproject_data["project"]["version"]
    except (FileNotFoundError, KeyError):
        return "0.0.1"


app = FastAPI(
    title="Inssider Crawler",
    description="인사이더 데이터 크롤링 및 조회 API",
    version=get_project_version(),
    contact={
        "name": "ooMia",
        "url": "http://github.com/ooMia",
        "email": "hyeonhak.kim.dev@gmail.com",
    },
)


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}
