import datetime

from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def session_creator():
    """Create a session key that is valid for 2 hours"""
    initial = f'sess_{get_random_string(10)}'
    session_expiration = (
        timezone.now() +
        datetime.timedelta(seconds=(120 * 60))
    )
    timestamp = session_expiration.timestamp()
    encoded_date = urlsafe_base64_encode(str(timestamp).encode('utf-8'))
    return initial + f'-{encoded_date}'


def session_is_valid(value: str):
    _, rhv = value.split('-')

    if rhv is None:
        return False

    timestamp = urlsafe_base64_decode(rhv).decode('utf-8')
    current_date = timezone.now()

    tz = timezone.get_current_timezone()
    expiration_date = datetime.datetime.fromtimestamp(
        float(timestamp),
        tz=tz
    )

    return False if current_date > expiration_date else True


def upload_to(instance, image_name):
    skin_color = instance.skin_color
    return f'faces/{skin_color.lower()}_{image_name}'


def create_id(prefix):
    return f'{prefix}_{get_random_string(10)}'


def astrologic_sign(date_of_birth: datetime.date | str | None, translate=False) -> str | None:
    if date_of_birth is None:
        return None

    if isinstance(date_of_birth, str):
        date_of_birth = datetime.datetime.strptime(
            date_of_birth,
            '%Y-%m-%d'
        ).date()

    shifts_to_next_year = ['Capricorne', 'Verseau', 'Poissons']

    dates = {
        'Bélier': [
            datetime.datetime(year=date_of_birth.year, month=3, day=20),
            datetime.datetime(year=date_of_birth.year, month=4, day=19)
        ],
        'Taureau': [
            datetime.datetime(year=date_of_birth.year, month=4, day=20),
            datetime.datetime(year=date_of_birth.year, month=5, day=20)
        ],
        'Gémeaux': [
            datetime.datetime(year=date_of_birth.year, month=5, day=21),
            datetime.datetime(year=date_of_birth.year, month=6, day=21)
        ],
        'Cancer': [
            datetime.datetime(year=date_of_birth.year, month=6, day=22),
            datetime.datetime(year=date_of_birth.year, month=7, day=22)
        ],
        'Lion': [
            datetime.datetime(year=date_of_birth.year, month=7, day=23),
            datetime.datetime(year=date_of_birth.year, month=8, day=22)
        ],
        'Vierge': [
            datetime.datetime(year=date_of_birth.year, month=8, day=23),
            datetime.datetime(year=date_of_birth.year, month=9, day=22)
        ],
        'Balance': [
            datetime.datetime(year=date_of_birth.year, month=9, day=23),
            datetime.datetime(year=date_of_birth.year, month=10, day=23)
        ],
        'Scorpion': [
            datetime.datetime(year=date_of_birth.year, month=10, day=24),
            datetime.datetime(year=date_of_birth.year, month=11, day=22)
        ],
        'Sagittaire': [
            datetime.datetime(year=date_of_birth.year, month=11, day=23),
            datetime.datetime(year=date_of_birth.year, month=12, day=22)
        ],
        'Capricorne': [
            datetime.datetime(year=date_of_birth.year, month=12, day=23),
            datetime.datetime(year=date_of_birth.year, month=1, day=20)
        ],
        'Verseau': [
            datetime.datetime(year=date_of_birth.year, month=1, day=21),
            datetime.datetime(year=date_of_birth.year, month=2, day=19)
        ],
        'Poissons': [
            datetime.datetime(year=date_of_birth.year, month=2, day=20),
            datetime.datetime(year=date_of_birth.year, month=3, day=20)
        ]
    }

    reset_year = False
    candidates = []
    for key, d in dates.items():
        start, end = d

        # When trying comparisions like 2000/1/1 > 2000/12/20
        # we get false, We have to shift the year of the
        # right (date of birth) to the next year in order
        # for the comparision to work effectively 2001/1/1 > 2000/12/20 -;
        # at the same time, we also need to replace the start year for all
        # signsthat are not Capricorne (which is the previous year - december)
        # and also the end year by moving them to the next year since the
        # date of birth would be on the next year
        if key in shifts_to_next_year:
            date_of_birth = date_of_birth.replace(year=date_of_birth.year + 1)
            if key != 'Capricorne':
                start = start.replace(year=date_of_birth.year)
            end = end.replace(year=date_of_birth.year)
            reset_year = True

        logic = [
            date_of_birth >= start.date(),
            date_of_birth <= end.date()
        ]

        if all(logic):
            candidates.append(key)

        if reset_year:
            # Replace does not create a copy of the date of birth
            # but increments the year to infinity so we need to
            # reset it to its initial value
            date_of_birth = date_of_birth.replace(year=date_of_birth.year - 1)

    if candidates:
        sign = candidates[-1]
        if translate:
            translations = {
                'Bélier': 'Aries',
                'Taureau': 'Taurus',
                'Gémeaux': 'Gemini',
                'Cancer': 'Cancer',
                'Lion': 'Leo',
                'Vierge': 'Virgo',
                'Balance': 'Libra',
                'Scorpion': 'Scorpio',
                'Sagittaire': 'Sagittarius',
                'Capricorne': 'Capricorn',
                'Verseau': 'Aquarius',
                'Poissons': 'Pisces'
            }
            return translations.get(sign)
        return sign
    return None
