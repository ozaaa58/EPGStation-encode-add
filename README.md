# EPGStation-encode-add
PythonとGitの勉強のために作ったもので、バグがあるかもしれません。

EPGStationのAPIを利用し、録画済み情報を取得、エンコードされていないものを
エンコードキューへ追加していくものです。
cron等に登録して深夜帯や日中にまとめてエンコードしたい場合に良いかと・・・

サーバーアドレス・エンコード情報など自分の環境に合わせ書き換えてください。

http://< server_addr >:< port >/api-docs/?url=/api/docs

上記URLでEPGStationのAPIが確認できます。各自必要に応じて参照願います。

WebAPIを叩くため”requests”ライブラリが必要です。

pip install requests

or

conda install requests

でライブラリをインストールしてください。
