from datetime import date


async def get_current_period(quarters):
    today = date.today()
    for quarter in quarters:
        if quarter.period_date_start <= today <= quarter.period_date_end:
            return quarter.period_date_start, quarter.period_date_end
    return None, None


async def get_full_year(quarters):
    if not quarters:
        return None, None
    return quarters[0].period_date_start, quarters[-1].period_date_end
