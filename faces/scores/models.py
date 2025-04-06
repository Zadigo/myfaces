import pathlib

from django.db import models
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from scores import validators
from scores.choices import Emotions, GenderChoices, SkinColor, ZodiacSigns
from scores.managers import FaceManager
from scores.utils import (astrologic_sign, session_creator, session_is_valid,
                          upload_to)


class UserDetail(models.Model):
    session = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=100
    )
    date_of_birth = models.DateField(
        validators=[validators.date_of_birth_validator]
    )
    zodiac_sign = models.CharField(
        max_length=150,
        choices=ZodiacSigns.choices,
        default=ZodiacSigns.LIBRA
    )
    ethnicity = models.CharField(
        max_length=100,
        validators=[validators.ethnicity_validator]
    )
    gender = models.CharField(
        max_length=100,
        choices=GenderChoices.choices,
        default=GenderChoices.OTHER,
        validators=[validators.gender_validator]
    )
    created_on = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'UserDetail: {self.pk}'

    @property
    def session_expired(self):
        """Checks if the session that was initially created
        by the user is still valid. This allows us to validate
        or invalidate the completion of scoring sessions"""
        return session_is_valid(self.session)


class Score(models.Model):
    user_detail = models.ForeignKey(
        UserDetail,
        models.SET_NULL,
        blank=True,
        null=True
    )
    score_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    image = models.ForeignKey(
        'Face',
        on_delete=models.SET_NULL,
        null=True
    )
    numeric = models.PositiveIntegerField(
        default=1,
        validators=[validators.numeric_score_validator]
    )
    emotion = models.CharField(
        max_length=100,
        choices=Emotions.choices(),
        default=Emotions.default('Not defined')
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Score: {self.score_id}'


class Face(models.Model):
    """Represents the actual face to rate"""

    image = models.ImageField(
        upload_to=upload_to
    )
    skin_color = models.CharField(
        max_length=100,
        choices=SkinColor.choices,
        default=SkinColor.BLACK
    )

    objects = FaceManager.as_manager()

    def __str__(self):
        return f'Face: {self.pk}'


@receiver(post_save, sender=UserDetail)
def evaluate_zodiac_sign(instance, created, **kwargs):
    if created:
        result = astrologic_sign(instance.date_of_birth)
        instance.zodiac_sign = result
        instance.save()


@receiver(pre_save, sender=Score)
def create_score_id(instance, **kwargs):
    if instance.score_id is None:
        instance.score_id = f'sc_{get_random_string(10)}'


@receiver(pre_save, sender=UserDetail)
def create_session_id(instance, **kwargs):
    instance.session = session_creator()


@receiver(pre_save, sender=Score)
def create_image_id(instance, **kwargs):
    instance.image_id = f'img_{get_random_string(10)}'


@receiver(pre_delete, sender=Face)
def delete_image(instance, **kwargs):
    if instance.image is not None:
        path = pathlib.Path(instance.image.path)
        try:
            path.unlink()
        except:
            pass
