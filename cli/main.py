import argparse

from cli.commands import _install, _serve, _test, _format


def entry_point():
    """웹 스크래핑을 위한 CLI 진입점"""
    parser = argparse.ArgumentParser(description="SNS Web Scraper")

    # 하위 명령어 파서 추가
    subparsers = parser.add_subparsers(dest="command", help="실행할 명령")

    # 각 명령어 모듈에서 파서 설정
    _install.setup_parser(subparsers)
    _test.setup_parser(subparsers)
    _serve.setup_parser(subparsers)
    _format.setup_parser(subparsers)

    args = parser.parse_args()

    match args.command:
        case "install":
            _install.handle_command(args)
        case "test":
            _test.handle_command(args)
        case "serve":
            _serve.handle_command(args)
        case "format":
            _format.handle_command(args)
        case _:
            parser.print_help()
            exit(1)


if __name__ == "__main__":
    entry_point()
