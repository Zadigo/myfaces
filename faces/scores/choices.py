from functools import cached_property
from django.db import models

POSITIVE_EMOTIONS = [
    'Loving',
    'Compationate',
    'Sympathic',
    'Intelligent',
    'Disciplined',
    'Stunning',
    'Lovely',
    'Adventurous',
    'Agreeable',
    'Ambitious',
    'Bright',
    'Charming',
    'Courageous',
    'Courteous',
    'Inventive',
    'Likable',
    'Passionate',
    'Sensible',
    'Trustworthy',
    'Witty',
    'Sleek',
    'Smooth',
    'Healthy',
    'Radiant',
    'Vibrant',
    'Polished',
    'Immaculate',
    'Seductive',
    'Heavenly',
    'Enchanting',
    'Happy',
    'Sincere',
    'Elegant',
    'Greedy'
]

NEGATIVE_EMOTIONS = [
    'Savage',
    'Uninteresting',
    'Annoying',
    'Freaky',
    'Jealous',
    'Money hungry',
    'Deceitful',
    'Impulsive',
    'Moody',
    'Narrow-minded',
    'Rude',
    'Unhappy',
    'Untrustworthy',
    'Coward',
    'Careless',
    'Bossy',
    'Arrogant',
    'Boastful',
    'Detached',
    'Egocentric',
    'Envious',
    'Narcissistic',
    'Petulant',
    'Vain',
    'Vindictive',
    'Bad-tempered',
    'Cynical',
    'Judgmental',
    'Intolerant',
    'Resentful',
    'Petty',
    'Unforgiving',
    'Unreachable',
    'Vulgar'
]


class SkinColor(models.Choices):
    BLACK = 'Black'
    WHITE = 'White'


# class Emotions(models.Choices):
#     NOT_DEFINED = 'Not defined'

#     LOVING = 'Loving'
#     COMPATIONATE = 'Compationate'
#     SYMPATHIC = 'Sympathic'
#     INTELLIGENT = 'Intelligent'
#     DISCIPLINED = 'Disciplined'
#     STUNNING = 'Stunning'
#     LOVELY = 'Lovely'
#     ADVENTUROUS = 'Adventurous'
#     AGREEABLE = 'Agreeable'
#     AMBITIOUS = 'Ambitious'
#     BRIGHT = 'Bright'
#     CHARMING = 'Charming'
#     COURAGEOUS = 'Courageous'
#     COURTEOUS = 'Courteous'
#     INVENTIVE = 'Inventive'
#     LIKABLE = 'Likable'
#     PASSIONATE = 'Passionate'
#     SENSIBLE = 'Sensible'
#     TRUSTWORTHY = 'Trustworthy'
#     WITTY = 'Witty'
#     SLEEK = 'Sleek'
#     SMOOTH = 'Smooth'
#     HEALTHY = 'Healthy'
#     RADIANT = 'Radiant'
#     VIBRANT = 'Vibrant'
#     POLISHED = 'Polished'
#     IMMACULATE = 'Immaculate'
#     SEDUCIVE = 'Seductive'
#     HEAVENLY = 'Heavenly'
#     ENCHANTING = 'Enchanting'
#     HAPPY = 'Happy'
#     SINCERE = 'Sincere'
#     ELEGANT = 'Elegant'
#     GREEDY = 'Greedy'

#     SAVAGE = 'Savage'
#     UNINTERESTING = 'Uninteresting'
#     ANNOYING = 'Annoying'
#     FREAKY = 'Freaky'
#     JEALOUS = 'Jealous'
#     MONEY_HUNGRY = 'Money hungry'
#     DECEITFUL = 'Deceitful'
#     IMPULSIVE = 'Impulsive'
#     MOODY = 'Moody'
#     NARROW_MINDED = 'Narrow-minded'
#     RUDE = 'Rude'
#     UNHAPPY = 'Unhappy'
#     UNTRUSTWORTHY = 'Untrustworthy'
#     COWARD = 'Coward'
#     CARELESS = 'Careless'
#     BOSSY = 'Bossy'
#     ARROGANT = 'Arrogant'
#     BOASTFUL = 'Boastful'
#     DETACHED = 'Detached'
#     EGOCENTRIC = 'Egocentric'
#     ENVIOUS = 'Envious'
#     NARCISSISTIC = 'Narcissistic'
#     PETULANT = 'Petulant'
#     VAIN = 'Vain'
#     VINDICTIVE = 'Vindictive'
#     BAD_TEMPERED = 'Bad-tempered'
#     CYNICAL = 'Cynical'
#     JUDGMENTAL = 'Judgmental'
#     INTOLERANT = 'Intolerant'
#     RESENTFUL = 'Resentful'
#     PETTY = 'Petty'
#     UNFORGIVING = 'Unforgiving'
#     UNREACHABLE = 'Unreachable'
#     VULGAR = 'Vulgar'


class Emotions:
    @classmethod
    def choices(self):
        emotions = POSITIVE_EMOTIONS + NEGATIVE_EMOTIONS
        emotions.extend(['Not defined'])
        return [(emotion, emotion) for emotion in emotions]

    @classmethod
    def default(cls, name):
        candidate = list(filter(lambda x: x[0] == name, cls.choices()))
        return candidate[-1]

    @classmethod
    def flatten(cls):
        return map(lambda x: x[0], cls.choices())

    @classmethod
    def as_dict(cls):
        count = len(POSITIVE_EMOTIONS + NEGATIVE_EMOTIONS)
        return {
            'count': count,
            'positive': sorted(POSITIVE_EMOTIONS),
            'negative': sorted(NEGATIVE_EMOTIONS)
        }


class GenderChoices(models.Choices):
    WOMAN = 'Woman'
    MAN = 'Man'
    OTHER = 'Other'


class ZodiacSigns(models.Choices):
    ARIES = 'Aries'
    TAURUS = 'Taurus'
    GEMINI = 'Gemini'
    CANCER = 'Cancer'
    LEO = 'Leo'
    VIRGO = 'Virgo'
    LIBRA = 'Libra'
    SCORPIO = 'Scorpio'
    SAGITTARIUS = 'Sagittarius'
    CAPRICORN = 'Capricorn'
    AQUARIUS = 'Aquarius'
    PISCES = 'Pisces'
