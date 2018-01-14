# https://github.com/websocket-client/websocket-client
import websocket
from threading import Thread
import time
import sys
import argparse

USER_NAME = ""
TEST_MODE = False


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):

        if USER_NAME and TEST_MODE:
            ws.send("TEST_MODE: " + USER_NAME)
        else:
            while True:
                raw = input()
                ws.send(raw)
    runThread = Thread(target=run)
    runThread.daemon = False
    runThread.start()

    def ping(*args):
        while True:
            time.sleep(1)
            ws.send("ping")

    Thread(target=ping).start()


if __name__ == "__main__":
    # websocket.enableTrace(True)
    parser = argparse.ArgumentParser(description='Arguments to start echoapp_client')
    parser.add_argument('--host', type=str, default="ws://voiceminder.localtunnel.me/websocket/",
                    help='an integer for the accumulator')
    parser.add_argument('--test', '-t', dest='test', action='store_true',
                    help='if argument is specified, puts the client in test mode')
    parser.add_argument('--name', '-n', required='--test' in sys.argv, type=str,
        help="specify the name of user to create socket if in test mode")
    args = parser.parse_args()
    host = args.host
    if args.test:
        TEST_MODE = args.test
        USER_NAME = args.name
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
