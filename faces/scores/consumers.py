import dataclasses
import random
from typing import Type

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.cache import cache
from scores import tasks
from scores.choices import Emotions
from scores.models import Face, Score, UserDetail
from scores.utils import session_creator, session_is_valid


@dataclasses.dataclass
class Score:
    face_id: int
    score: int
    image: str = None
    emotion: str = None

    def __hash__(self):
        return hash(self.face)


class FaceManager:
    NUMBER_OF_LEVELS = 3
    NUMBER_OF_IMAGES = 10

    def __init__(self):
        self.session_id = None
        self.current_index = 1
        self.current_level = 1
        self.consumer: AsyncJsonWebsocketConsumer | None = None
        # Contains all the faces of the database
        # to simplify local usage
        self.faces = []
        self.selected_faces = []
        # Container used to pop the faces that
        # we want to return
        self.destructive_container = []
        self._local_scores: list[Score] = []

    def __get__(self, instance, cls=None):
        self.consumer = instance
        return self

    @database_sync_to_async
    def get_faces(self):
        qs = cache.get('faces', None)
        if qs is None:
            qs = Face.objects.all()
            cache.set('face', qs, timeout=(30 * 60))

        values = qs.values('id', 'image', 'skin_color')
        self.faces = list(values)

    @property
    def black_women(self):
        return list(filter(lambda x: x['skin_color'] == 'Black', self.faces))

    @property
    def white_women(self):
        return list(filter(lambda x: x['skin_color'] == 'White', self.faces))

    async def get_session_id(self):
        self.session_id = session_creator()
        return self.session_id

    async def select_faces(self):
        """Get all the faces from the database and then
        make a selection of faces to be used for rating"""
        if not self.faces:
            await self.get_faces()

        random_black_women = random.sample(self.black_women, self.NUMBER_OF_IMAGES)
        random_white_women = random.sample(self.white_women, self.NUMBER_OF_IMAGES)

        self.selected_faces = random_black_women + random_white_women
        self.destructive_container.extend(self.selected_faces)

        random.shuffle(self.destructive_container)

    async def get_face(self):
        if not self.destructive_container:
            await self.select_faces()

        # TODO: Save the current face selection with
        # the current sessionId. The selection will
        # be trashed once the full session is over
        # in order to preven incomplete data

        return self.destructive_container.pop()

    async def finalize(self):
        """Function that needs to called once a score
        is added because it allows us to know the current index
        and level for the current scoring session"""
        self.current_index += 1

        # When he have reached the level determined by
        # the maximum level, then reset the whole system
        # because the scoring is over
        if self.current_level == self.NUMBER_OF_LEVELS:
            self.current_index = 1
            self.current_level = 1
            await self.consumer.send_json({'action': 'scoring.finished'})

        if self.current_index > 10:
            self.current_index = 1
            self.current_level += 1
            # Repopulate the descructive container with
            # new images for the next level
            self.destructive_container.extend(self.selected_faces)
            await self.consumer.send_json({'action': 'next.level', 'level': self.current_level})
        
        await self.consumer.send_json({'action': 'update.index', 'index': self.current_index})


    async def add_score(self, face_id: int, score: int):
        """Adds a numeric score to the current face"""
        self._local_scores.append(Score(face_id, score))
        tasks.add_score.apply_async(
            (
                self.session_id, 
                face_id, 
                score
            ), 
            countdown=3
        )
        await self.finalize()

    async def add_emotion(self, face_id: int, emotion: str):
        """Adds an emotion score to the current face"""
        if not self._local_scores:
            return await self.consumer.send_json({
                'action': 'error',
                'messge': 'No initial scores were sent'
            })

        candidates: list[Score] = list(
            filter(
                lambda x: x['id'] == face_id,
                self._local_scores
            )
        )

        if candidates:
            face = candidates[0]
            face.emotion = emotion
        await self.finalize()


class FaceConsumer(AsyncJsonWebsocketConsumer):
    manager = FaceManager()

    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        await self.send_json({'action': 'websocket.close'})
        await self.close(code=1000)

    async def receive_json(self, content, **kwargs):
        action = content['action']

        if action == 'get.session_id':
            session_id = await self.manager.get_session_id()
            await self.send_json({
                'action': 'get.session_id',
                'token': session_id
            })

        if action == 'set.session_id':
            previous_session_id = content.get('session_id', None)
            if previous_session_id is None:
                return
            
            if self.manager.session_id:
                if previous_session_id == self.manager.session_id:
                    return
                
            is_active = session_is_valid(previous_session_id)
            self.manager.session = previous_session_id

        if action == 'save.score':
            face_id = content['face_id']
            score = content['score']
            await self.manager.add_score(face_id, score)

            face = await self.manager.get_face()
            await self.send_json({
                'action': 'random.face',
                'data': face
            })

        if action == 'random.face':
            face = await self.manager.get_face()
            await self.send_json({
                'action': 'random.face',
                'data': face
            })

        if action == 'get.emotions':
            print(Emotions.as_dict())
            await self.send_json({
                'action': 'get.emotions',
                'data': Emotions.as_dict()
            })

        if action == 'get.faces':
            await self.manager.select_faces()
            await self.send_json(
                {
                    'action': 'get.faces',
                    'results': self.manager.selected_faces,
                    'session_id': await self.manager.get_session_id()
                }
            )

        if action == 'get.emotions':
            await self.send_json({
                'action': 'get.emotions',
                'results': Emotions.as_dict()
            })
