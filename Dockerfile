# Dockerfile

# 1. ベースとなるPythonイメージを指定
# Python 3.11-alpine に変更
FROM python:3.11-alpine

RUN apk update \
    && apk add --no-cache \
       postgresql-client \
       postgresql-dev \
       build-base

# 2. 必要なライブラリをインストール
# 重複しているpostgresql-client, postgresql-dev, build-baseは削除しても良い
RUN apk add --no-cache \
    libffi-dev \
    musl-dev \
    gcc \
    python3-dev \
    libpq \
    jpeg-dev \
    zlib-dev \
    tzdata

# 3. タイムゾーンを設定 (これはwebコンテナのOSタイムゾーン)
# docker-compose.ymlでTZ=UTCを設定しているので、ここでの設定は冗長になる可能性もありますが、
# コンテナ内のデフォルトを確実にしたい場合は残しても良いです。
# ただし、Djangoアプリ側でAsia/Tokyoを使用したい場合は、この設定は不要です。
# 私は docker-compose.yml で web サービスにも TZ=UTC を設定する推奨の方針に従い、
# ここは削除して、webコンテナ全体をUTCで動かすことを推奨します。
# ENV TZ=Asia/Tokyo # ★削除を推奨★

# 4. 作業ディレクトリを設定
WORKDIR /app

# 5. まず requirements.txt だけをコピーして、ライブラリをインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. 次に、entrypoint.sh をコピーして実行権限を与える
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# 7. 最後に、アプリケーションのコード全体をコピー
COPY . .

# 8. コンテナ起動時の入り口として entrypoint.sh を指定
ENTRYPOINT ["entrypoint.sh"]

# 9. 公開するポートを指定
EXPOSE 8000

# 10. entrypoint.sh に渡すデフォルトのコマンドを指定
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]