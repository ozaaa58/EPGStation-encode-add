ARG PYTHON_BASE_IMAGE='python'

FROM ${PYTHON_BASE_IMAGE}:3.11 AS rye

# Pythonがpycファイルを書き込まないようにします。
ENV PYTHONDONTWRITEBYTECODE=1

# Pythonがstdoutとstderrをバッファリングしないようにします。これにより、
# バッファリングによりログが発生せずにアプリケーションがクラッシュする状況を避けることができます。
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH="/app/src:$PYTHONPATH"

# 仮想環境はryeが実行されるワーキングディレクトリで作成されるため、
# 開発環境と本番環境はそれぞれ同一のディレクトリにする必要があります。
WORKDIR /app

RUN \
    --mount=type=cache,target=/var/lib/apt/lists \
    --mount=type=cache,target=/var/cache/apt/archives \
    apt-get update \
    && apt-get install -y --no-install-recommends build-essential

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

# RYE_INSTALL_OPTIONはビルドに必要です。
# 参照: https://github.com/mitsuhiko/rye/issues/246
RUN curl -sSf https://rye-up.com/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash

# Dockerのキャッシュを利用するために、依存関係のダウンロードを別のステップとして行います。
# バインドマウントを利用して一部のファイルをこのレイヤーにコピーすることを避けます。
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=requirements.lock,target=requirements.lock \
    --mount=type=bind,source=requirements-dev.lock,target=requirements-dev.lock \
    --mount=type=bind,source=.python-version,target=.python-version \
    --mount=type=bind,source=README.md,target=README.md \
    rye sync --no-dev --no-lock

RUN . .venv/bin/activate

# 本番用のステージ
FROM rye AS run

# アプリケーションが実行する非特権ユーザーを作成します。
# 参照: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=1000
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# アプリケーションを実行するために非特権ユーザーに切り替えます。
USER appuser

COPY . .

ENTRYPOINT ["python3", "./src/EPGStation-encode-add.py"]