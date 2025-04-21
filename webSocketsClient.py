import websocket
import _thread
import rel
import sys

def on_message(ws, message):
    print(message)
    if message in ('Compiling IAR success.', 'error code 1'):
        rel.abort()

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print(f"### closed ### Status: {close_status_code}, Msg: {close_msg}")

def on_open(ws):
    print("Opened connection")
    if len(sys.argv) > 1:
        def run():
            ws.send(sys.argv[1])
        _thread.start_new_thread(run, ())
    else:
        ws.send("IAR Compile")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("Your websocket server & port", # Ex. ws://192.168.1.1:8765"
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()