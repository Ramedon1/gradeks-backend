async def get_full_year(quarters):
    if not quarters:
        return None, None
    return quarters[0].quarter_date_start, quarters[-1].quarter_date_end
