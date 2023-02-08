from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
)
import os

app = Flask(__name__)

# チャネルシークレットを設定
YOUR_CHANNEL_SECRET = "068bfe3b390715f2fa1461512a57b262"
# チャネルアクセストークンを設定
YOUR_CHANNEL_ACCESS_TOKEN = "5t37s0AS/pzavLZ6dTGnje32Xk16S/7KVtTd8C4FgN8SzSknNscqiSYnY1gJGtODBoWrtnJsDl7YALEhwc0oFrOvTr/hHTJE23FfIfq/zQWX2kbzT0SQulym/w7vEOVe9Ixwc4Z2rAY7Unraafu2twdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# https://line-bot-kojimayuushi-2.onrender.com/callback にアクセスされたら以下の関数を実行する
@app.route("/callback", methods=['POST'])
def callback():
    # アクセス時に送られてきたデータ「X-Line-Signature」を代入
    signature = request.headers['X-Line-Signature']

    # アクセス時に送られてきたデータの主な部分を代入
    body = request.get_data(as_text=True)

    # try 内でエラーが発生したら except の文を実行
    try:
        # ハンドラーに定義されている関数を呼び出す
        handler.handle(body, signature)
    # もし「InvalidSigunatureError」というエラーが発生したら、以下のプログラムを実行
    except InvalidSignatureError:
        # リクエストを送った側に400番(悪いリクエストですよー！)を返す
        abort(400)

    # すべて順調にいけば、リクエストを送った側に「OK」と返す
    return "OK"

# ハンドラーに定義されている関数
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ここにメッセージの内容による処理を書いていこう

    # メッセージの種類が「テキスト」なら
    if event.type == "message":
        response_message = ""

        # event.message.text という変数にメッセージの内容が入っている
        if (event.message.text == "おはよう") or (event.message.text == "おはよ"):
            response_message = "太陽えぇ感じや。オレと太陽ニアピンやから見間違えたらあかんで♡"

        elif (event.message.text == "ひろと") or (event.message.text == "ひろちゃん"):
            response_message = "まま！？これは違うねん。ヌンチャクの練習するからこれは無駄使いじゃないねん。。💦"

        elif (event.message.text == "しね") or (event.message.text == "死ね"):
            response_message = "あぁぁあぁ（光悦）"

        elif (event.message.text == "遊ぼ") or (event.message.text == "あそぼー"):
            response_message = "え～、また平成の坂登るんか～（うれしい）"
        
        elif (event.message.text == "おやすみ") or (event.message.text == "おやすみー"):
            response_message = "まぁ、夢にもでてくるからずっと一緒やけどな💗   え～ろい"

        else:
            response_message = "え？オレのこと好きってこと？それはタイツやわ～！え～ろい"

        # 返信文を送信
        # response_message の中に入っている文を返す
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=response_message)
            ]
        )

# ポート番号を環境変数から取得
port = os.getenv("PORT")
app.run(host="0.0.0.0", port=port)

