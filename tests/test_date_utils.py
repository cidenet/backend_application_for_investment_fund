# tests/test_date_utils.py
from datetime import datetime
from app.utils.formater.date_utils import DateUtils

def test_format_datetime():
    dt = datetime(2023, 1, 1, 12, 0, 0)
    formatted_date = DateUtils.format_datetime(dt)
    assert formatted_date == "2023-01-01 12:00:00"

    formatted_date_custom = DateUtils.format_datetime(dt, "%d/%m/%Y %H:%M:%S")
    assert formatted_date_custom == "01/01/2023 12:00:00"