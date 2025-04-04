import datetime
from django.core.exceptions import ValidationError


def numeric_score_validator(value):
    if value < 1 or value > 5:
        raise ValidationError('Score should be between 1 and 5')


def date_of_birth_validator(value):
    eighteen_at = datetime.datetime.now().date().year - 18
    d = datetime.datetime(day=31, month=12, year=eighteen_at)
    if value > d.date():
        raise ValidationError("User should be eighteen and over")


def gender_validator(value):
    genders = ['Woman', 'Man', 'Other']
    if value not in genders:
        raise ValidationError('Gender should be one of Woman, Man or other')


def ethnicity_validator(value):
    if value not in ['Black', 'White']:
        raise ValidationError('Ethnicity should be either black or white')
