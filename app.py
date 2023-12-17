# coding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import chatbot
#line token
channel_access_token = 'G3l1mLCs/oQ0b3K0YywjYO/1NJN3MCpkItVwSVmxBLzjav9Er6XZ38YswKFVybrURmD0VX5uZIJrakrbZRRJtZdNOAwKpvPMJuIeCM7WZ3NF3PmnYcMKpqBDO9elbFW1UEctFNb5LZNLk3Za46NjvAdB04t89/1O/w1cDnyilFU='
channel_secret = 'ba5cbc8df30a57ea62f2e6acc7938671'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

# 監聽所有來自 /callback 的 Post Request
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
    #echo
    # msg= event.message.text
    msg = chatbot.get_response(event.message.text)
    message = TextSendMessage(text=msg)
    line_bot_api.reply_message(event.reply_token,message)
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)