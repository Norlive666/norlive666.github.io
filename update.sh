#!/usr/bin/env bash
# T大帅的个人网站快速更新入口
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$DIR/site_manager.py" "$@"
