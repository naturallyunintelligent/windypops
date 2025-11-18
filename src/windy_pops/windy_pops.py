import os
import sys

import numpy as np
from tabulate import tabulate

import windy_pops.evaluator as evaluator
from windy_pops.constants import (INTERVAL_LENGTH_MINUTES, LIGHTNING_LIMIT,
                                  LOCATIONS, MAX_WIND_SPEED, MIN_WIND_SPEED,
                                  MINIMUM_WINDOW_DURATION)
from windy_pops.data_loader import Metoffice_dataloader
from windy_pops.evaluator import (assert_if_datapoint_is_safe_overall,
                                  filter_for_useable_safe_subsequences,
                                  find_contiguous_safe_periods_in)
from windy_pops.time_utils import weekly_forecast
from windy_pops.vector2d import Vector2D

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging

logger = logging.getLogger("main_logger")


def configure_logging_to_file() -> None:
    logger.setLevel(logging.ERROR)

    file_handler = logging.FileHandler(
        "/Users/std3ldn/repos_gitlab_five/windy-pops/error.log"
    )
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def display_to_user(weekly_forecast_datapoints) -> None:
    print(tabulate(weekly_forecast_datapoints, headers=["Start", "End", "Day"]))


def evaluate_forecast_datapoint(forecast_datapoint, shoreham_coast_normal):
    wind_vector = convert_wind_to_vector(forecast_datapoint)
    score_dict = {
        # '2024-09-03T09:00Z'
        "time": np.datetime64(forecast_datapoint["time"]),
        "datapoint_scores": {
            "daylight_score": evaluator.evaluate_daylight(
                forecast_datapoint["time"], LOCATIONS["shoreham_beach"]
            ),
            "wind_direction": evaluator.evaluate_wind_direction(
                wind_vector=wind_vector, coast_normal=shoreham_coast_normal
            ),
            "wind_speed": evaluator.evaluate_wind_speed(
                wind_vector=wind_vector,
                wind_gust=forecast_datapoint["windGustSpeed10m"],
                max_wind_speed=MAX_WIND_SPEED,
                min_wind_speed=MIN_WIND_SPEED,
            ),
            "lightning": evaluator.evaluate_lightning(
                prob_of_sferics=forecast_datapoint["probOfSferics"],
                lightning_limit=LIGHTNING_LIMIT,
            ),
        },
    }
    return score_dict


def convert_wind_to_vector(forecast_datapoint):
    wind_vector = Vector2D.from_bearing_and_magnitude(
        bearing=forecast_datapoint["windDirectionFrom10m"],
        magnitude=forecast_datapoint["windSpeed10m"],
    )
    return wind_vector


def main(data_loader=Metoffice_dataloader(), use_datafile=False) -> list[list[str]]:
    if use_datafile:
        weather_data = data_loader.get_weather_forecast(use_cache=True)
    else:
        weather_data = data_loader.data

    shoreham_coast_normal = Vector2D.from_bearing_and_magnitude(
        bearing=180, magnitude=1
    )

    scores = []
    safety_evaluated_forecast_datapoints = []
    for i, forecast_datapoint in enumerate(
        weather_data["features"][0]["properties"]["timeSeries"]
    ):
        scores.append(
            evaluate_forecast_datapoint(forecast_datapoint, shoreham_coast_normal)
        )
        safety_evaluated_forecast_datapoints.append(
            assert_if_datapoint_is_safe_overall(scores[i])
        )

    safe_subsequences = find_contiguous_safe_periods_in(
        safety_evaluated_forecast_datapoints
    )
    valid_safe_subsequences = filter_for_useable_safe_subsequences(
        safe_subsequences, INTERVAL_LENGTH_MINUTES, MINIMUM_WINDOW_DURATION
    )
    weekly_forecast_datapoints = weekly_forecast(valid_safe_subsequences)
    display_to_user(weekly_forecast_datapoints)

    return weekly_forecast_datapoints


configure_logging_to_file()
try:
    main()
except Exception as e:
    logger.error("An error occurred", exc_info=True)
