import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '505001941:AAEBqXUFJxckLS_oEa5qbzx4Wt1-Kt8W9ZA'
WEBHOOK_URL = 'https://fe08941d.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'init',
        'introduction',
        'youtube',
        'google',
        'baidu',
        'google_pic',
        'print_text'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'introduction',
            'dest': 'youtube',
            'conditions': 'is_going_to_youtube'
        },
        {
            'trigger': 'advance',
            'source': 'youtube',
            'dest': 'print_text',
            'conditions': 'is_going_to_print_text'
        },
        {
            'trigger': 'advance',
            'source': 'introduction',
            'dest': 'google',
            'conditions': 'is_going_to_google'
        },
        {
            'trigger': 'advance',
            'source': 'google',
            'dest': 'print_text',
            'conditions': 'is_going_to_print_text'
        },
        {
            'trigger': 'advance',
            'source': 'introduction',
            'dest': 'baidu',
            'conditions': 'is_going_to_baidu'
        },
        {
            'trigger': 'advance',
            'source': 'baidu',
            'dest': 'print_text',
            'conditions': 'is_going_to_print_text'
        },
        {
            'trigger': 'advance',
            'source': 'introduction',
            'dest': 'google_pic',
            'conditions': 'is_going_to_google_pic'
        },
        {
            'trigger': 'advance',
            'source': 'google_pic',
            'dest': 'print_text',
            'conditions': 'is_going_to_print_text'
        },
        {
            'trigger': 'go_back',
            'source': [
                'print_text',
            ],
            'dest': 'introduction'
        },
        {
            'trigger': 'advance',
            'source': [
                'init'
            ],
            'dest': 'introduction',
            'conditions': 'start'
        }
    ],
    initial='init',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
