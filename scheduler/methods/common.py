async def get_full_year(quarters):
    if not quarters:
        return None, None
    return quarters[0].period_date_start, quarters[-1].period_date_end
