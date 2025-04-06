from celery import shared_task
from celery.utils.log import get_logger
from scores.models import Face, Score, UserDetail

logger = get_logger('scores')


@shared_task
def add_score(session_id: str, face_id: int, score: int):
    try:
        face = Face.objects.get(id=face_id)
    except:
        logger.error('Face does not exist')
        return

    try:
        user_detail = UserDetail.objects.get(session=session_id)
    except:
        logger.error('User detail does not exist')
        return
    else:
        score = Score.objects.create(
            user_detail=user_detail,
            image=face,
            numeric=score
        )
        return score.id
