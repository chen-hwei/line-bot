from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('pK+ndtyQe9slsrA1kzH/KObUOx0mID1sm8uw6PfuM8+4YHZLowqBEkEX8W41pSEQqJbLd7iAX1TIM/ozpPP0kIEcPCFsF0RKJqReLcaHady3CgOLanSRmjpccYQi/uSc8RvtxYxboJO56c0vssvHoQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5dd107fa5bc981d534cea0dc30837850')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()