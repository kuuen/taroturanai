from transformers import T5Tokenizer, AutoModelForCausalLM
import os
import sys
import cgi
import json

import torch
# ソケットライブラリ取り込み
import socket


tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt-1b")
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-1b")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# prompt = "人生を楽しくポジティブに生きていくための3つのこと。1."
prompt = "夜の魚取"

def generete(prompt):

    input_ids = tokenizer.encode(prompt, return_tensors="pt",add_special_tokens=False).to(device)
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=250,
            min_length=200,
            do_sample=True,
            top_k=500,
            top_p=0.95,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            bad_word_ids=[[tokenizer.unk_token_id]],
            # num_return_sequences=5
            num_return_sequences=1
        )
    decoded = tokenizer.batch_decode(output,skip_special_tokens=True)
    # for i in range(5):
    #     print(decoded[i])
    print(decoded[0])
    return decoded


# サーバーIPとポート番号
IPADDR = "127.0.0.1"
PORT = 4922

# AF_INET：IPv4形式でソケット作成(省略可)
sock_sv = socket.socket(socket.AF_INET)
# IPアドレスとポート番号でバインド、タプルで指定
sock_sv.bind((IPADDR, PORT))
# サーバー有効化
sock_sv.listen()

print("start")

# 接続・受信の無限ループ
while True:
    # クライアントの接続受付
    sock_cl, addr = sock_sv.accept()
    # ソケットから byte 形式でデータ受信
    data = sock_cl.recv(1024)
    print(data.decode("utf-8"))

    a = json.loads(data.decode("utf-8"))
    print(a['msg'])
    result = generete(a['msg'])[0]

    # キーワードを削除する
    result = result.lstrip(a['msg'])
    result = result[: result.rfind('。')]

    sock_cl.send(result.encode('utf-8'))

    # クライアントのソケットを閉じる
    sock_cl.close()