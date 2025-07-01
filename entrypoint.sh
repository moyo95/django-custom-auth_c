#!/bin/sh

# ファイルのパーミッションを変更する（エラーが出ても処理を続行する）
chmod -R a+r app accounts mysite templates static manage.py || true

# DjangoのWebサーバーを起動する
# exec "$@" は、CMDで渡されたコマンドを実行するという意味
exec "$@"