import random
from django.core.cache import cache
from django.db.models import QuerySet

from scores.choices import SkinColor


class FaceManager(QuerySet):
    def _create_sample(self, queryset, size=5):
        if not queryset.exists():
            return []
        
        # Returns 5 faces from each batch
        black_girls = queryset.filter(skin_color='Black')
        white_girls = queryset.filter(skin_color='White')

        ids1 = list(black_girls.values_list('id', flat=True))
        ids2 = list(white_girls.values_list('id', flat=True))
        
        try:
            random_ids = [*random.sample(ids1, size), *random.sample(ids2, size)]
        except:
            return []
        else:
            return [item for item in queryset if item.id in random_ids]

    def cached_all(self):
        queryset = cache.get('faces', None)
        if queryset is None:
            queryset = self.all()
            cache.set('faces', queryset, 3600)
        return queryset

    def sample_faces(self, size=5):
        if isinstance(size, str):
            if size.isnumeric():
                size = int(size)
            else:
                size = 5
        queryset = self.all()
        return self._create_sample(queryset, size=size)
