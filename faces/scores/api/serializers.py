from django.shortcuts import get_object_or_404
from rest_framework import fields
from rest_framework.serializers import Serializer
from scores.choices import Emotions, GenderChoices, SkinColor
from scores.models import Face, Score, UserDetail
from scores.utils import create_id
from scores.validators import numeric_score_validator


class ScoreSerializer(Serializer):
    image = fields.IntegerField()
    numeric = fields.IntegerField(validators=[numeric_score_validator])
    emotion = fields.ChoiceField(
        Emotions.choices(),
        default=Emotions.default('Not defined')
    )


class ValidateNewSession(Serializer):
    session = fields.CharField(read_only=True)
    country = fields.CharField()
    date_of_birth = fields.DateField()
    ethnicity = fields.ChoiceField(
        choices=SkinColor.choices,
        default='Black'
    )
    gender = fields.ChoiceField(
        choices=GenderChoices.choices,
        default='Other'
    )

    def create(self, validated_data):
        return UserDetail.objects.create(**validated_data)


class ValidateScoreSerializer(Serializer):
    """Validates the list of scores that
    were created by the user"""

    session = fields.CharField(allow_null=True)
    scores = ScoreSerializer(many=True)

    def create(self, validated_data):
        session_id = validated_data['session']
        user_detail = get_object_or_404(UserDetail, session=session_id)

        if not user_detail.session_expired:
            items_to_create = []
            for item in validated_data['scores']:
                image = get_object_or_404(Face, id=item['image'])
                data_to_save = {
                    'image': image,
                    'numeric': item['numeric'],
                    'emotion': item['emotion'],
                    'user_detail': user_detail
                }
                items_to_create.append(Score(**data_to_save))
            return Score.objects.bulk_create(items_to_create)
        return []


class FaceSerializer(Serializer):
    id = fields.IntegerField(read_only=True)
    image = fields.ImageField()
    skin_color = fields.CharField()


class ValidateUserDetails(Serializer):
    country = fields.CharField()
    date_of_birth = fields.CharField()
    gender = fields.CharField()
    ethnicity = fields.CharField()


class ValidateSession(Serializer):
    session = fields.CharField(read_only=True)
    session_expired = fields.BooleanField()
