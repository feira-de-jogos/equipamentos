from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid, environ):
    await sio.enter_room(sid, "chat_users")
    print("connect ", sid)


@sio.on("state")
async def state(sid, data):
    print("message ", data)
    await sio.emit("state", data, room="chat_users")


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


if __name__ == "__main__":
    web.run_app(app)
