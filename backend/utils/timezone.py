from datetime import datetime, timezone as date_timezone, timedelta

import pytz

from backend.core.conf import settings


class TimeZone:
    """时区工具类"""

    def __init__(self, tz: str = settings.DATETIME_TIMEZONE):
        self.tz_info = pytz.timezone(tz)

    def now(self) -> datetime:
        """获取当前时间（带时区）"""
        return datetime.now(self.tz_info)

    def from_datetime(self, dt: datetime) -> datetime:
        """转换 datetime 到当前时区"""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=date_timezone.utc)
        return dt.astimezone(self.tz_info)

    def to_str(self, dt: datetime, fmt: str = settings.DATETIME_FORMAT) -> str:
        """datetime 转字符串"""
        if dt.tzinfo is None:
            dt = self.from_datetime(dt)
        return dt.strftime(fmt)

    def from_str(self, date_str: str, fmt: str = settings.DATETIME_FORMAT) -> datetime:
        """字符串转 datetime（带时区）"""
        dt = datetime.strptime(date_str, fmt)
        return self.tz_info.localize(dt)

    def to_utc(self, dt: datetime) -> datetime:
        """转换到 UTC"""
        if dt.tzinfo is None:
            dt = self.tz_info.localize(dt)
        return dt.astimezone(date_timezone.utc)

    @property
    def utc_offset(self) -> timedelta:
        """获取当前时区偏移"""
        return self.tz_info.utcoffset(self.now())


# 全局时区实例
timezone = TimeZone()
