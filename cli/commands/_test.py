import subprocess


def run_tests(all_tests=False):
    """단위 테스트를 실행합니다"""
    try:
        subprocess.run(["pytest", "--sw"], check=True)
    except KeyboardInterrupt:
        pass


def setup_parser(subparsers):
    """test 명령어 파서를 설정합니다"""
    parser = subparsers.add_parser("test", help="단위 테스트 실행")
    parser.add_argument(
        "--all", action="store_true", help="모든 테스트 파일 실행 (통합 테스트 포함)"
    )
    return parser


def handle_command(args):
    """test 명령어 처리"""
    run_tests(all_tests=getattr(args, "all", False))
