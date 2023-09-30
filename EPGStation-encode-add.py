#!/usr/bin/env python
# coding: utf-8

import requests
import json
import datetime
import codecs
import yaml
import logging

# configファイルの読み込み
with open("config.yaml", "r") as yml:
    config: dict = yaml.safe_load(yml)

# サーバーアドレスを取得
server_addr: str = config["server_addr"]

# エンコードオプションを取得
enc_option = config["enc_option"]
# directoryオプションが設定されていない場合は要素を削除
if enc_option["directory"] == "None":
    enc_option.pop("directory")

# ログの設定
logging.basicConfig(
    level=config["log_level"],
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a",  # ログの出力モード ('w': 上書き, 'a': 追記)
)

# ログ出力インスタンスを作成する。引数にログ出力名称を設定する。
logger = logging.getLogger("Logging")

# ログを標準出力する。
sh = logging.StreamHandler()
logger.addHandler(sh)


# エンコードキューへ追加する関数
def enc(rec_id, vid_id, enc_option):
    enc_api_url = server_addr + "/api/encode"  # エンコードAPI-URLを設定

    # IDを設定
    enc_option.update(recordedId=rec_id, sourceVideoFileId=vid_id)

    # APIからエンコードキューに追加
    enc_api = requests.post(enc_api_url, json=enc_option)
    enc_add_result = enc_api.json()

    # 結果の確認
    if "encodeId" in enc_add_result:
        logger.info(f"Success! : {enc_add_result}")
        result_code = 0
    else:
        logger.error(f"Failure! : {enc_add_result}")
        result_code = 1

    return result_code


# エンコードキュー情報を取得
enc_cue_api = server_addr + "/api/encode?isHalfWidth=true"
enc_cue = requests.get(enc_cue_api)
enc_cue_json = enc_cue.json()

# 録画リスト情報を取得
rec_list_api = (
    server_addr
    + "/api/recorded?isHalfWidth=true&offset=0&limit="
    + str(config["limit"])
)
rec_list = requests.get(rec_list_api)
rec_list_json = rec_list.json()

# 既にエンコードキューにあるのプログラムIDを取得
in_progress: list = []
if len(enc_cue_json["runningItems"]) != 0:
    in_progress.append(enc_cue_json["runningItems"][0]["recorded"]["id"])
    if len(enc_cue_json["waitItems"]) != 0:
        for s in range(len(enc_cue_json["waitItems"])):
            in_progress.append(enc_cue_json["waitItems"][s]["recorded"]["id"])

# エンコードキューに追加するプログラムIDを取得
for i in range(len(rec_list_json["records"])):
    program_info = rec_list_json["records"][i]
    rec_file_info = program_info["videoFiles"]

    # videoFilesの要素数で処理を分岐
    # 要素数が2つ以上の場合はエンコードファイルが存在している可能性が高いため処理しない
    if len(rec_file_info) == 1:
        file_type = rec_file_info[0]["type"]
        # FileTypeがTSかどうかを確認
        if file_type == "ts":
            rec_id = program_info["id"]
            vid_id = rec_file_info[0]["id"]
            if len(in_progress) != 0:
                if rec_id in in_progress:
                    logger.info(
                        f"ProgramID:{rec_id} This ProgramID is already in the encode cue"
                    )
                else:
                    logger.info(f"ProgramID: {rec_id} VideoID: {vid_id} is encode-add")
                    enc(rec_id, vid_id, enc_option)
            else:
                logger.info(f"ProgramID: {rec_id} VideoID: {vid_id} is encode-add")
                enc(rec_id, vid_id, enc_option)

        else:
            pass

    else:
        pass

#        file_type= []
#        for j in range(len(rec_file_info)):
#            file_type.append(rec_file_info[j]["type"])
#        if "encoded" in file_type:
#            print("no-encode")
#        else:
#            pass
