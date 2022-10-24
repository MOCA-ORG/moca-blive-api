from fastapi import FastAPI
from fastapi.websockets import WebSocket
from ..blivedm import BLiveClient
from ..handlers import WebSocketHandler
from ..libs import *
from os import environ


SECRET_KEY: str = environ.get('SECRET_KEY', 'change_me')
app: FastAPI = FastAPI()


@app.websocket('/live')
async def live_endpoint(websocket: WebSocket):
    """获取信息信息"""
    await websocket.accept()
    while True:
        init_msg: dict = await websocket.receive_json()

        try:
            certification: str = init_msg['secret_key']
            room_id: str = init_msg['room_id']

            if certification != SECRET_KEY:
                await websocket.send_text('Invalid Certification.')
                await websocket.close()
                return None
        except KeyError:
            await websocket.send_text('Invalid Usage.')
            await websocket.close()
            return None

        client: BLiveClient = BLiveClient(room_id, opts={'WS': websocket})
        client.add_handler(WebSocketHandler())
        client.start()
        await client.join()
