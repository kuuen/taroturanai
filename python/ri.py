from transformers import T5Tokenizer, AutoModelForCausalLM
import json
import torch
# ソケットライブラリ取り込み
import socket
import logging
import bleach
 
#ロガーの生成
logger = logging.getLogger('mylog')
#出力レベルの設定
logger.setLevel(logging.INFO)
#ハンドラの生成
handler = logging.FileHandler('log/log.log')
#ロガーにハンドラを登録
logger.addHandler(handler)
#フォーマッタの生成
fmt = logging.Formatter('%(asctime)s %(message)s')

handler.setFormatter(fmt)


tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt-1b")
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-1b")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# prompt = "人生を楽しくポジティブに生きていくための3つのこと。1."
prompt = "夜の魚取"

def generete(prompt, min_length, max_length):

    input_ids = tokenizer.encode(prompt, return_tensors="pt",add_special_tokens=False).to(device)
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            min_length=min_length,
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
    # print(decoded[0])
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

    logger.info('受付')

    # ソケットから byte 形式でデータ受信
    data = sock_cl.recv(2048)
    # print(data.decode("utf-8"))

    try :
        a = json.loads(data.decode("utf-8"))
    except UnicodeDecodeError : 
        re = {
            "msg" : 'よくわからなかった。',
            "item" : ''
        }
        sock_cl.send(json.dumps(re).encode('utf-8'))
        sock_cl.close()
        continue
    except json.decoder.JSONDecodeError:
        re = {
            "msg" : 'よくわからなかった。',
            "item" : ''
        }
        sock_cl.send(json.dumps(re).encode('utf-8'))
        sock_cl.close()
        continue

    msg = 'おくら'
    if ("msg" in a) :
        # HTMLエスケープ処理
        msg = bleach.clean(a['msg'], strip=True)

    min = len(msg)
    if ("min" in a) :
        try :
            v = int(a["min"])
            if v > 5:
                min = v
        except ValueError:
            min = min

    max = len(msg)
    if ("max" in a) :
        try :
            # v = len(msg) + int(a["max"])
            v = int(a["max"])
            if v > 15:
                max = v
        except ValueError:
            max = max + 10

    if max < min:
        max = min

    # print(a['msg'])
    result = generete(msg, min, max)[0]

    # s = a['msg'] + 'ラッキーアイテムは'
    # l = len(s)
    # item = generete(s, l + 5, l + 15)[0]
    # item = generete(s, 5, l + 15)[0]

    # 結果キーワードを削除する
    result = result.lstrip(a['msg'])
    result = result[: result.rfind('。')]

    # ラッキーアイテムキーワードを削除する
    # item = item.lstrip(s)

    re = {
        "msg" : result
    }

    # sock_cl.send(result.encode('utf-8'))
    sock_cl.send(json.dumps(re).encode('utf-8'))

    # クライアントのソケットを閉じる
    sock_cl.close()
