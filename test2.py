import websocket
import time
import threading

from threadpool import ThreadPool, makeRequests

SERVER_URL = "ws://dev.ingress-performance-test-websocket.stg.svc.qt-k8s-hz.com/ws"


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
    def send_thread():
        send_info = {"seq": "0_0", "cmd": "ping", "data": {}}
        while True:
            time.sleep(5)
            ws.send(json.dumps(send_info))

    t = threading.Thread(target=send_thread)
    t.start()


def on_start():
    # time.sleep(2)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(SERVER_URL,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    init_logging()
    pool = ThreadPool(50000)
    test = list()
    for ir in range(50000):
        test.append(ir)
    requests = makeRequests(on_start, test)
    [pool.putRequest(req) for req in requests]
    pool.wait()
