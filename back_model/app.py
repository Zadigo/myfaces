import asyncio
import datetime

import pandas
from quart import Quart, websocket
from quart_cors import cors

app = Quart(__name__)
app_cors = cors(
    app,
    allow_origin=[
        'http://localhost:5173',
        'http://localhost:8100'
    ]
)


class GraphCalculator:
    scores = []

    async def register_score(self, image, score):
        self.scores.append({
            'date': str(datetime.datetime.now()),
            'image': image,
            'score': score
        })


async def calculate_date():
    while True:
        # d = datetime.datetime.now()
        # await websocket.send_json({'type': 'update.time', 'date': str(d)})
        await asyncio.sleep(15)


async def receiver(instance):
    while True:
        try:
            message = await websocket.receive_json()
        except asyncio.TimeoutError:
            await websocket.close(1)
        else:
            if message['type'] == 'register.score':
                await instance.register_score(message['image'], message['score'])


@app.websocket('/ws/scrutiner')
async def scrutiner():
    await websocket.accept()
    calculator = GraphCalculator()

    t1 = asyncio.create_task(calculate_date())
    t2 = asyncio.create_task(receiver(calculator))

    while True:
        await t1
        await t2


if __name__ == '__main__':
    app.run(debug=True)
