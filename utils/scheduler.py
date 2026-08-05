from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import calendar


class WipeScheduler:
    """
    Calculates Rust wipe dates.
    """

    def __init__(self):
        pass


    def clean_timezone(self, timezone: str):
        """
        Fix common timezone formatting mistakes.
        """

        timezone = timezone.strip()

        # Fix lowercase first letter
        parts = timezone.split("/")

        if len(parts) == 2:
            timezone = (
                parts[0].title()
                + "/"
                + parts[1].replace("_", " ").title().replace(" ", "_")
            )

        return timezone


    def get_next_weekly(
        self,
        weekday: int,
        time: str,
        timezone: str,
        start_date=None
    ):

        timezone = self.clean_timezone(timezone)

        tz = ZoneInfo(timezone)

        now = start_date or datetime.now(tz)

        hour, minute = map(int, time.split(":"))

        target = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        days_ahead = weekday - now.weekday()

        if days_ahead < 0:
            days_ahead += 7

        target += timedelta(days=days_ahead)

        if target <= now:
            target += timedelta(days=7)

        return target



    def get_next_monthly(
        self,
        week: str,
        weekday: int,
        time: str,
        timezone: str,
        start_date=None
    ):

        timezone = self.clean_timezone(timezone)

        tz = ZoneInfo(timezone)

        now = start_date or datetime.now(tz)

        week = week.lower().strip()

        hour, minute = map(int, time.split(":"))

        year = now.year
        month = now.month


        while True:

            days_in_month = calendar.monthrange(
                year,
                month
            )[1]

            dates = []


            for day in range(1, days_in_month + 1):

                date = datetime(
                    year,
                    month,
                    day,
                    hour,
                    minute,
                    tzinfo=tz
                )

                if date.weekday() == weekday:
                    dates.append(date)


            if week == "first":
                result = dates[0]

            elif week == "second":
                result = dates[1]

            elif week == "third":
                result = dates[2]

            elif week == "fourth":
                result = dates[3]

            elif week == "last":
                result = dates[-1]

            else:
                raise ValueError(
                    f"Invalid week: {week}"
                )


            if result > now:
                return result


            if month == 12:
                year += 1
                month = 1
            else:
                month += 1



    def get_next_wipes(
        self,
        schedule_type: str,
        week: str,
        weekday: int,
        time: str,
        timezone: str
    ):

        schedule_type = schedule_type.lower().strip()

        timezone = self.clean_timezone(timezone)

        tz = ZoneInfo(timezone)


        first_check = datetime.now(tz)

        results = []


        for _ in range(2):

            if schedule_type == "weekly":

                wipe = self.get_next_weekly(
                    weekday,
                    time,
                    timezone,
                    first_check
                )


            elif schedule_type == "monthly":

                wipe = self.get_next_monthly(
                    week,
                    weekday,
                    time,
                    timezone,
                    first_check
                )


            else:
                raise ValueError(
                    f"Invalid schedule type: {schedule_type}"
                )


            results.append(wipe)

            first_check = wipe + timedelta(seconds=1)


        return results[0], results[1]