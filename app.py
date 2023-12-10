# coding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

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
    msg='https://www.google.com/maps/dir/24.8244389,121.7022625/24.6748671,121.675608/24.6118089,121.6365653/24.7603435,121.7534132/24.8434334,121.7820505/24.8164107,121.8217512/24.8686561,121.8327408/24.6427251,121.7330825/24.7139177,121.6885279/24.7536907,121.750255/@24.80845,121.6350792,11.26z?entry=ttu'
    message = TextSendMessage(text=msg)
    line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)