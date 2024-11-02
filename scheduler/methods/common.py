from datetime import date


async def get_current_period(quarters):
    today = date.today()
    for quarter in quarters:
        if quarter.quarter_date_start <= today <= quarter.quarter_date_end:
            return quarter.quarter_date_start, quarter.quarter_date_end
    return None, None


async def get_full_year(quarters):
    if not quarters:
        return None, None
    return quarters[0].quarter_date_start, quarters[-1].quarter_date_end
