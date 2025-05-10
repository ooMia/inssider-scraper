import subprocess


def setup_parser(subparsers):
    subparsers.add_parser("format", help="코드 포맷팅 (black, autoflake)")


def handle_command(args):
    subprocess.run(["black", "."], check=True)
    subprocess.run(["autoflake", "."], check=True)
    # [ ] TODO move to lint command
    subprocess.run(
        ["flake8", ".", "--extend-exclude", ".venv", "--max-line-length", "100"], check=False
    )
