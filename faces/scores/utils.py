from collections import OrderedDict
import datetime
from django.utils.crypto import get_random_string
from functools import lru_cache


def upload_to(instance, image_name):
    skin_color = instance.skin_color
    return f'faces/{skin_color.lower()}_{image_name}'


def create_id(prefix):
    return f'{prefix}_{get_random_string(10)}'


class Zodiac:
    def __init__(self):
        self.dates = {
            'Bélier': ('21 march', '20 april'),
            'Taureau': ('21 april', '21 may'),
            'Gémeaux': ('22 may', '21 june'),
            'Cancer': ('22 june', '22 july'),
            'Lion': ('23 july', '22 august'),
            'Vierge': ('23 august', '22 september'),
            'Balance': ('23 september', '22 october'),
            'Scorpion': ('23 october', '22 november'),
            'Sagittaire': ('23 november', '21 december'),
            'Capricorne': ('22 december', '20 january'),
            'Verseau': ('21 january', '19 february'),
            'Poissons': ('20 february', '20 march')
        }

        self.current_date = datetime.datetime.now()
        self.arranged_dates = self.create_dates()

    @lru_cache(maxsize=100)
    def create_dates(self):
        arranged_dates = OrderedDict()
        for key, value in self.dates.items():
            lhv, rhv = value

            lhv_date = datetime.datetime.strptime(lhv, '%d %B')
            rhv_date = datetime.datetime.strptime(rhv, '%d %B')

            lhv_date = lhv_date.replace(year=self.current_date.year)

            if key == 'Capricorne':
                rhv_date = rhv_date.replace(year=self.current_date.year + 1)
                arranged_dates[key] = (lhv_date, rhv_date)
                continue

            rhv_date = rhv_date.replace(year=self.current_date.year)
            arranged_dates[key] = (lhv_date, rhv_date)
        return arranged_dates

    def translate(self, sign):
        signs = {
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
        return signs[sign]

    def evaluate_date_of_birth(self, d):
        if isinstance(d, str):
            d = datetime.datetime.strptime(d, '%Y-%m-%d')
        
        # Normalize the date to the current year so that
        # we can compare them below to the zodiac dates
        d = d.replace(year=self.current_date.year)

        candidate = []
        for key, value in self.arranged_dates.items():
            lhv, rhv = value

            if d >= lhv.date() and d <= rhv.date():
                candidate.append(self.translate(key))
                candidate.append((lhv, rhv))
                break
        return candidate
