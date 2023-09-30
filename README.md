# EPGStation-encode-add

Python と Git の勉強のために作ったもので、バグがあるかもしれません。

EPGStation の API を利用し、録画済み情報を取得、エンコードされていないものを
エンコードキューへ追加していくものです。
cron 等に登録して深夜帯や日中にまとめてエンコードしたい場合に。

サーバーアドレス・エンコード情報など自分の環境に合わせ `config.yaml` 書き換えてください。

`http://< server_addr >:< port >/api-docs/?url=/api/docs`

上記 URL で EPGStation の API が確認できます。各自必要に応じて参照願います。

WebAPI を叩くため `requests` ライブラリが必要です。

`pip install requests` or `conda install requests` でライブラリをインストールしてください。
