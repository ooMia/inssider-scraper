import subprocess


def install_dev():
    """개발 환경으로 패키지를 설치합니다"""
    subprocess.run(["pip", "install", "-e", ".[dev]"], check=True)


def setup_parser(subparsers):
    """install 명령어 파서를 설정합니다"""
    parser = subparsers.add_parser("install", help="개발 환경으로 패키지 설치")
    return parser


def handle_command(args):
    """install 명령어 처리"""
    install_dev()
