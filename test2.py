import websocket
import time
import json
import threading

from threadpool import ThreadPool, makeRequests

SERVER_URL = "ws://dev.ingress-performance-test-websocket.stg.svc.qt-k8s-hz.com/ws"

total = 0


def on_message(ws, message):
    print(message)
    pass


def on_error(ws, error):
    print(error)
    pass


def on_close(ws):
    print("### closed ###")
    pass


def on_open(ws):

    global total

    def send_thread():
        send_info = {"seq": "0_0", "cmd": "ping", "data": {}}
        while True:
            time.sleep(5)
            ws.send(json.dumps(send_info))
            print("send msg to server")

    t = threading.Thread(target=send_thread)
    t.start()
    total += 1
    print("一共启动连接: {}", total)


def on_start(t):
    time.sleep(0.05)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(SERVER_URL,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    pool = ThreadPool(1000)
    test = list()
    for ir in range(1000):
        test.append(ir)
    requests = makeRequests(on_start, test)
    [pool.putRequest(req) for req in requests]
    pool.wait()
