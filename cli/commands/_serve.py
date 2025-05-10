import subprocess


def serve_app(port=None):
    """FastAPI 애플리케이션을 실행합니다"""
    cmd = ["uvicorn", "controller.main:app", "--reload"]
    if port:
        cmd.extend(["--port", str(port)])
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        pass


def setup_parser(subparsers):
    """serve 명령어 파서를 설정합니다"""
    parser = subparsers.add_parser("serve", help="FastAPI 애플리케이션 실행")
    parser.add_argument("-p", "--port", type=int, help="서버 포트 지정")
    return parser


def handle_command(args):
    """serve 명령어 처리"""
    serve_app(args.port)
