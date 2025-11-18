import datetime as datetime

import numpy as np
import pandas as pd
from astral import LocationInfo
from astral.sun import sunrise, sunset

# this is WIP - thinking about how to handle date and time consistently without duplication
# def parse_iso_datetime(iso_date_str: str) -> datetime.date, datetime.time:
#     dt = datetime.datetime.strptime(iso_date_str, "%Y-%m-%dT%H:%M%z")
#     return dt.date(), dt.time()


def sunrise_and_sunset(date_str: str, location: dict) -> tuple[str, str]:
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    city = LocationInfo(latitude=location["lat"], longitude=location["lon"])
    sunrise_time = sunrise(city.observer, date=dt)
    sunset_time = sunset(city.observer, date=dt)
    return sunrise_time, sunset_time


def time_difference_minutes(t_1: np.datetime64, t_2: np.datetime64) -> float:
    return float((t_2 - t_1) / np.timedelta64(1, "m"))


def weekly_forecast(valid_safe_subsequences):
    weekly_forecast_datapoints = []
    for time_window in valid_safe_subsequences:
        # day_of_the_week_int = (pd.Timestamp(time_window[0])).to_pydatetime().weekday()
        # day_of_the_week = calendar.day_name[day_of_the_week_int]
        # # day_of_the_week = datetime.datetime.strftime(day_of_the_week, "%A")
        day_of_the_week = datetime.datetime.strftime(
            (pd.Timestamp(time_window[0])).to_pydatetime(), "%A"
        )
        weekly_forecast_datapoints.append(
            [day_of_the_week, time_window[0], time_window[1]]
        )
    print("weekly_forecast_datapoints:" + str(weekly_forecast_datapoints))
    return weekly_forecast_datapoints
