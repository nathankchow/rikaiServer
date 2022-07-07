from multiprocessing import Process
import eventlet
import socketio
import pyperclip
import time
eventlet.monkey_patch()
import subprocess
import socket

#get ip address
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

ip_address = get_ip()
port = 8088

mgr = socketio.KombuManager("amqp://")
write_only = socketio.KombuManager("amqp://", write_only=True)
sio = socketio.Server(logger=True, engineio_logger=True, client_manager=mgr)

app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'public/index.html'}
})

global emitting
emitting = False

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    global emitting
    if emitting==False:
        sio.start_background_task(emitter) #make sure only one instance of emitter is running 
        emitting=True
    else:
        print("already emitting!")

@sio.event
def my_message(sid, data):
    print('message ', data)
    return "GOt your my message bro."

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
def test(sid, data):
    print('test', data)

def listener(sio,app):
    print("Server started.")
    eventlet.wsgi.server(eventlet.listen((ip_address, port)), app)
    print("Listener function unexpectedly terminated?")

def emitter():
    previous = pyperclip.paste()
    while True:
        current = pyperclip.paste()
        if current != previous:
            print(f"{current}")
            sio.emit('message', {'data': current})
            eventlet.sleep(0)
            print("starting background task")
            p = Process(target=emit_info_from_kombu, args=(current,))
            p.start()
            previous = current 
        else:
            pass 
        eventlet.sleep(0.10)
 

def emit_info_from_kombu(msg):
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info = subprocess.Popen(f"ichiran-cli -i {msg}", startupinfo=si, stdout=subprocess.PIPE)
        print("popen terminated")
        lines_iterator = iter(info.stdout.readline, b"")
        s = ''
        for line in lines_iterator:
            s+=(line.decode())
        info = s
    except:
        info = "Error: ichiran-cli failed to return expected output. Possible cause is inclusion of a number in the text query (e.g. 2時間)."
    write_only.emit('segmented', {
        "raw" : msg,
        "info": info
    })

def main():
    listener(sio,app)

if __name__ == '__main__':
    main()
