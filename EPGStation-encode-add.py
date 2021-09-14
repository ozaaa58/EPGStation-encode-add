#!/usr/bin/env python
# coding: utf-8

# In[69]:


import requests
import json
import datetime
import codecs


# In[70]:


server_addr = "http://localhost:8888"

def enc(rec_id,vid_id):
    enc_api_url = server_addr + "/api/encode"
    enc_option = {"recordedId": rec_id,
                  "sourceVideoFileId": vid_id,
                  "parentDir": "encoded-2",
                  #"directory": "string",
                  "isSaveSameDirectory": False,
                  "mode": "H.264",
                  "removeOriginal": False}

    enc_api = requests.post(enc_api_url, json=enc_option)
    enc_add_result = enc_api.json()
    if'encodeId' in enc_add_result:
        print("Success! :",enc_add_result)
        print("Success! :",enc_add_result,end="\n", file=codecs.open('log.txt', 'a', 'utf-8'))

    else:
        print("Failure! :",enc_add_result)
        print("Failure! :",enc_add_result,end="\n", file=codecs.open('log.txt', 'a', 'utf-8'))

print(datetime.datetime.now())
print(datetime.datetime.now(),end="\n", file=codecs.open('log.txt', 'a', 'utf-8'))

enc_cue_api = server_addr + "/api/encode?isHalfWidth=true"
enc_cue = requests.get(enc_cue_api)
enc_cue_json = enc_cue.json()

rec_list_api = server_addr + "/api/recorded?isHalfWidth=true&offset=0&limit=500"
rec_list = requests.get(rec_list_api)
rec_list_json = rec_list.json()

in_progress = []

if len(enc_cue_json["runningItems"]) != 0:
    in_progress.append(enc_cue_json["runningItems"][0]["recorded"]["id"])
    if len(enc_cue_json["waitItems"]) != 0:
        for s in range(len(enc_cue_json["waitItems"])):
            in_progress.append(enc_cue_json["waitItems"][s]["recorded"]["id"])

for i in range(len(rec_list_json["records"])):
    program_info = rec_list_json["records"][i]
    rec_file_info = program_info["videoFiles"]

    if len(rec_file_info) == 1:
        file_type = rec_file_info[0]["type"]
        if file_type == "ts":
            rec_id = program_info["id"]
            vid_id = rec_file_info[0]["id"]
            if len(in_progress) != 0:
                if rec_id in in_progress:
                    print("ProgramID:",rec_id," This ProgramID is already in the encode cue")
                    print("ProgramID:",rec_id," This ProgramID is already in the encode cue",end="\n", file=codecs.open('log.txt', 'a', 'utf-8'))
                else:
                    print("ProgramID:",rec_id,"VideoID:",vid_id,"is encode-add")
                    print("ProgramID:",rec_id,"VideoID:",vid_id,"is encode-add",end="\n", file=codecs.open('log.txt', 'a', 'utf-8'))
                    enc(rec_id,vid_id)
            else:
                print("ProgramID:",rec_id,"VideoID:",vid_id,"is encode-add")
                print("ProgramID:",rec_id,"VideoID:",vid_id,"is encode-add",end="\n", file=codecs.open('log.txt', 'a', 'utf-8'))
                enc(rec_id,vid_id)

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


# In[ ]:




