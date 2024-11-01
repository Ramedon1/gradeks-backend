from datetime import date


async def get_current_period(quarters):
    today = date.today()
    for quarter in quarters:
        if quarter.quarter_date_start <= today <= quarter.quarter_date_end:
            return quarter.quarter_date_start, quarter.quarter_date_end
    return None, None
