#!/bin/bash

# 1. 현재 파일 경로 및 파일명 저장
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TARGET="cron.sh"

# 2. cron 작업 등록 (조건부)
if crontab -l | grep -q "$DIR/$TARGET"; then
    echo "Cron job already exists"
else
    (crontab -l ; echo "*/10 * * * * $DIR/$TARGET") | crontab -
    echo "Cron job added"
fi

# 3. 실행
source "$DIR/.venv/bin/activate"
python3 "$DIR/main.py"