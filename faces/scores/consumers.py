import asyncio
import datetime
import random

from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode
from scores.choices import Emotions
from scores.models import Face, Score, UserDetail


class FaceManager:
    def __init__(self, consumer):
        self.consumer = consumer
        self.faces = []
        self.selected_faces = []

    @database_sync_to_async
    def get_faces(self):
        qs = Face.objects.all()
        self.faces = list(qs.values('id', 'image', 'skin_color'))

    @database_sync_to_async
    def add_scores(self, scores):
        for item in scores:
            try:
                face = Face.objects.get(id=item['image'])
            except:
                self.consumer.send_json(
                    {
                        'type': 'error',
                        'message': 'Face does not exist'
                    }
                )
                return False

            user_detail = UserDetail.objects.first()
            score = Score.objects.create(
                user_detail=user_detail, 
                image=face, 
                numeric=item['score']
            )

    async def get_session_id(self):
        initial = f'sess_{get_random_string(length=10)}'
        session_expiration = (
            timezone.now() +
            datetime.timedelta(seconds=7200)
        )
        timestamp = session_expiration.timestamp()
        encoded_date = urlsafe_base64_encode(str(timestamp).encode('utf-8'))
        return initial + f'-{encoded_date}'

    async def select_faces(self, k=10):
        if not self.faces:
            await self.get_faces()

        self.selected_faces = random.sample(self.faces, k)

    async def shuffle_existing_faces(self):
        pass

    async def add_emotion(self):
        pass

    async def entrypoint(self):
        pass


class FaceConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = FaceManager(self)

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.send_json({'type': 'websocket.close'})
        await self.close(code=close_code)

    async def receive_json(self, content, **kwargs):
        if content['type'] == 'get.faces':
            await self.manager.select_faces()
            await self.send_json(
                {
                    'type': 'get.faces',
                    'results': self.manager.selected_faces,
                    'session_id': await self.manager.get_session_id()
                }
            )

        if content['type'] == 'get.emotions':
            self.send_json({
                'type': 'get.emotions',
                'results': Emotions.as_dict()
            })

        if content['type'] == 'save.scores':
            await self.manager.add_scores(content['scores'])

        await self.send_json({'status': 'ok'})
