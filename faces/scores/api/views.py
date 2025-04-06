import random

from django.db.models.aggregates import Avg
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema, inline_serializer)
from rest_framework import fields, status
from rest_framework.decorators import api_view
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     ListAPIView, RetrieveAPIView)
from rest_framework.response import Response
from scores.api import serializers
from scores.api.serializers import (FaceSerializer, ValidateScoreSerializer,
                                    ValidateUserDetails)
from scores.choices import Emotions
from scores.models import Face, Score, UserDetail
from scores.utils import session_creator

EMOTIONS_PARAMS = [
    OpenApiParameter(
        'count',
        type=int
    ),
    OpenApiParameter(
        'positive',
        type=list,
        many=True,
        description='List of positive emotions'
    ),
    OpenApiParameter(
        'negative',
        type=list,
        many=True,
        description='List of negative emotions'
    )
]

EMOTIONS_EXAMPLES = [
    OpenApiExample(
        'count',
        value=1
    ),
    OpenApiExample(
        'positive',
        value=[
            "Adventurous",
            "Agreeable",
            "Ambitious",
            "Bright"
        ],
        response_only=True
    ),
    OpenApiExample(
        'negative',
        value=[
            "Annoying",
            "Arrogant",
            "Bad-tempered",
            "Boastful"
        ],
        response_only=True
    )
]

EMOTIONS_RESPONSE = inline_serializer(
    'emotions',
    fields={
        'count': fields.IntegerField(),
        'positive': fields.ListField(),
        'negative': fields.ListField()
    }
)


@extend_schema(operation_id='Faces')
class ListAllFaces(ListAPIView):
    """List all the faces that are available
    in the database"""

    queryset = Face.objects.cached_all()
    serializer_class = serializers.FaceSerializer


@extend_schema(operation_id='Random Faces')
class ListRandomFaces(ListAPIView):
    """List a set of random faces to be rated
    from the database"""

    queryset = Face.objects.cached_all()
    serializer_class = serializers.FaceSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        size = self.request.GET.get('size', 5)
        return Face.objects.sample_faces(size=size)


@extend_schema(operation_id='Emotions', responses=EMOTIONS_RESPONSE, parameters=EMOTIONS_PARAMS, examples=EMOTIONS_EXAMPLES)
class ListEmotions(ListAPIView):
    """Returns the list of positive and negative
    emotions that can be used to evaluate a face"""

    def list(self, request, *args, **kwargs):
        return Response(data=Emotions.as_dict())


@extend_schema(operation_id='Submit Scores')
class SubmitScores(CreateAPIView):
    serializer_class = serializers.ValidateScoreSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return_response = {'count': 0}
        return Response(return_response, status=status.HTTP_201_CREATED)


@api_view(['get'])
def ranking_view(request, **kwargs):
    response_data = {}
    queryset = Score.objects.all()
    ranking = queryset.annotate(average_score=Avg('numeric'))
    ranking_values = ranking.values('id', 'image__image', 'average_score')
    response_data['ranking'] = sorted(
        ranking_values,
        key=lambda x: -x['average_score']
    )
    return Response(data=response_data)


@extend_schema(operation_id='New Session')
class CreateNewSession(CreateAPIView):
    """Creates new scoring session for the current user"""

    serializer_class = serializers.ValidateNewSession


class NewSessionKey(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({'token': session_creator()})


@extend_schema(operation_id='Validate Session')
class SessionValidity(RetrieveAPIView):
    """Validates whether the user can continue
    his scoring session in the provided timeframe"""

    lookup_field = 'session'
    lookup_url_kwarg = 'session'
    queryset = UserDetail.objects.all()
    serializer_class = serializers.ValidateSession
