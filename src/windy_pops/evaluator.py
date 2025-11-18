from datetime import datetime
from itertools import groupby

from windy_pops.time_utils import sunrise_and_sunset, time_difference_minutes
from windy_pops.vector2d import Vector2D

EvaluationResult = tuple[bool, float | None]


def evaluate_daylight(time: str, location: str) -> EvaluationResult:
    fmt_string = "%Y-%m-%dT%H:%M%z"
    time_datetime = datetime.strptime(time, fmt_string)
    date = time.split("T")[0]
    sunrise_time, sunset_time = sunrise_and_sunset(date, location)
    within_daylight = sunrise_time < time_datetime < sunset_time
    return within_daylight, None


def evaluate_wind_direction(
    wind_vector: Vector2D, coast_normal: Vector2D
) -> EvaluationResult:
    # as a start, anything Northerly considered off-shore and so windsafe would be false
    # NOTE: wind direction is the bearing of where the wind is coming FROM
    wind_safe = wind_vector.dot(coast_normal) <= 0
    if wind_safe:
        cross_shore_score = (
            -wind_vector.normalised().dot(coast_normal.normalised()) * 10
        )  # will need to do something complicated here
    else:
        cross_shore_score = None
    return wind_safe, cross_shore_score


def evaluate_wind_speed(
    wind_vector: Vector2D,
    wind_gust: float,
    max_wind_speed: float,
    min_wind_speed: float,
) -> EvaluationResult:
    # wind speed is in m/s
    # wind gust is an absolute speed in m/s
    wind_speed = wind_vector.magnitude()
    if wind_gust < wind_speed:
        raise ValueError("Wind gust cannot be less than wind speed")
    wind_score = None
    wind_viable = min_wind_speed < wind_speed < max_wind_speed
    if wind_viable:
        wind_score = 10 - ((wind_gust - wind_speed) / wind_speed) * 10
    return wind_viable, wind_score


def evaluate_lightning(prob_of_sferics, lightning_limit) -> EvaluationResult:
    # prob_of_sferics is % chance of a lightning strike within 50km
    lightning_safe_boolean = prob_of_sferics < lightning_limit
    return lightning_safe_boolean, prob_of_sferics


def assert_if_datapoint_is_safe_overall(score_dict):
    print("____________________")
    print(f"Assessing, {score_dict['time']}")
    for name, result in score_dict["datapoint_scores"].items():
        if result[0] is False:
            print(f"{name} is not safe")

    return score_dict["time"], all(
        [evaluator[0] for evaluator in score_dict["datapoint_scores"].values()]
    )


def find_contiguous_safe_periods_in(safety_list):
    safe_subsequences = [
        [elt[0] for elt in subsequence]
        for is_safe, subsequence in groupby(safety_list, lambda x: x[1])
        if is_safe
    ]
    return safe_subsequences


def filter_for_useable_safe_subsequences(
    safe_subsequences, interval_length_minutes: int, minimum_duration_minutes: int
) -> list:
    valid_safe_subsequences = [
        (subsequence[0], subsequence[-1])
        for subsequence in filter(
            lambda x: time_difference_minutes(x[0], x[-1]) + interval_length_minutes / 2
            >= minimum_duration_minutes,
            safe_subsequences,
        )
    ]
    return valid_safe_subsequences
