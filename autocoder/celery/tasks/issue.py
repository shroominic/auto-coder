from ..worker import celery


@celery.task(name="solve_issue")
def solve_issue(issue_id: int) -> bool:
    """ Solve issue queued by user """
    pass

@celery.task(name="solve_revision")
def solve_revision(issue_id: int) -> bool:
    """ Solve revision queued by user """
    pass
