from datetime import datetime


class DateUtils:
    @staticmethod
    def format_datetime(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        return dt.strftime(format)
