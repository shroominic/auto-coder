from ..worker import celery


@celery.task(name="search_bug")
def search_bug(repository_id: int) -> bool:
    """ Search for bugs in repository """
    pass

@celery.task(name="suggest_issues")
def suggest_issues(repository_id: int) -> bool:
    """ Suggest issues for repository """
    pass
