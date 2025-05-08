import subprocess


def run_tests():
    """단위 테스트를 실행합니다"""
    subprocess.run(["python", "-m", "unittest", "discover", "-f"], check=True)


def setup_parser(subparsers):
    """test 명령어 파서를 설정합니다"""
    parser = subparsers.add_parser("test", help="단위 테스트 실행")
    return parser


def handle_command(args):
    """test 명령어 처리"""
    run_tests()
