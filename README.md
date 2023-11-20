# EPGStation-encode-add

Python と Git の勉強のために作ったもので、バグがあるかもしれません。  
EPGStation の API を利用し、録画済み情報を取得、エンコードされていないものを
エンコードキューへ追加していく Python スクリプトです。  
cron 等に登録して深夜帯や日中にまとめてエンコードしたいと言った用途を想定しています。

`config.yaml.sample` を `config.yaml` へ変更し、サーバーアドレス・エンコード情報など自分の環境に合わせ書き換えてください。  
`http://<IP>:<Port>/api-docs/?url=/api/docs`  
上記 URL で EPGStation の API が確認できます。各自必要に応じて参照し、適切に設定してください。

WebAPI を叩くため `requests` ライブラリが必要です。  
`pip install requests` or `conda install requests` でライブラリをインストールしてください。
Rye を利用している場合は`rye sync --no-dev`で依存パッケージを導入できます。

Docker を利用する場合は適宜 UID 等を環境に合わせ利用してください。
