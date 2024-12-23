from datetime import datetime


def invester(source, targets):
    """Инвестирование пожертвований в проекты."""
    used_targets = []
    for target in targets:
        contribution = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount,
        )
        target.invested_amount += contribution
        source.invested_amount += contribution
        if target.full_amount == target.invested_amount:
            target.fully_invested = True
            target.close_date = datetime.now()
        used_targets.append(target)
        if source.full_amount == source.invested_amount:
            source.fully_invested = True
            source.close_date = datetime.now()
            break
    return source, used_targets
