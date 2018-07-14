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

line_bot_api = LineBotApi('D5zmjYetfV7482lFZ5msn6Hj9Y+VaEAX3RBES4vpuRve95JdrYQpSQM/75WKGzftIxm5Arg0mZDBFfL+YCmCI3LkivQ4AM/7B/0qbJ0WlshA/vbAtZ1IIZbUTBTBY/wccb4noxJQoRTqYYI6DO9d6QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5533fb8aca896458aeadb8db06d9b714')


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()