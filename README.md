# taroturanai
タロット占い

カードの画像データは別途用意する

## 環境構築方法  
Anacondaをインストール  
  
Anaconda Prompt (anaconda3)を起動、以下をインストール  
  
### Huggingface Transformersのインストール  
conda install transformers  
  
### Sentencepieceのインストール  
conda install sentencepiece  


conda install bleach

apacheをphp動作できるように設定する
  
  
## 実行方法
Anaconda Prompt (anaconda3)にてri.pyを実行して受信待ち状態にする  
初回起動はかなり時間がかかる  
「start」が出力されたら準備完了  
例：  
>python C:\doc\占い\result\ri.py  
(ポート4922を開けておく。多分TCP)  
  
pythonフォルダ以外をwebサーバのドキュメントルートに設置  
apacheで動作確認できた

## チャットサーバーの起動
cd taroturanai/chat
php bin/server.php &