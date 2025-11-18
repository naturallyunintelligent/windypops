import numpy as np
import pytest

from windy_pops.constants import LIGHTNING_LIMIT, LOCATIONS
from windy_pops.evaluator import (EvaluationResult,
                                  assert_if_datapoint_is_safe_overall,
                                  evaluate_daylight, evaluate_lightning,
                                  evaluate_wind_direction, evaluate_wind_speed)
from windy_pops.vector2d import Vector2D

lightning_safe_value = LIGHTNING_LIMIT - 1
lightning_not_safe_value = LIGHTNING_LIMIT + 1


@pytest.mark.parametrize(
    ["time", "evaluation_result"],
    [
        # daylight is safe
        ("2024-10-22T12:00Z", EvaluationResult((True, None))),
        # night time is not safe
        ("2024-10-22T23:00Z", EvaluationResult((False, None))),
    ],
)
def test_evaluate_daylight(time: str, evaluation_result: EvaluationResult) -> None:
    result = evaluate_daylight(time=time, location=LOCATIONS["shoreham_beach"])
    assert result == evaluation_result


@pytest.mark.parametrize(
    ["prob_of_sferics", "lightning_limit", "evaluation_result"],
    [
        # Safe lightning evaluation
        (lightning_safe_value, LIGHTNING_LIMIT, True),
        # Not safe lightning evaluation
        (lightning_not_safe_value, LIGHTNING_LIMIT, False),
    ],
)
def test_evaluate_lightning(
    prob_of_sferics, lightning_limit, evaluation_result: EvaluationResult
) -> None:
    assert evaluate_lightning(prob_of_sferics, lightning_limit)[0] == evaluation_result


@pytest.mark.parametrize(
    ["wind_vector", "coast_normal", "evaluation_result"],
    [
        # On-shore wind is safe
        (
            Vector2D.from_bearing_and_magnitude(bearing=0, magnitude=1),
            Vector2D.from_bearing_and_magnitude(bearing=180, magnitude=1),
            EvaluationResult((True, 10.0)),
        )
        # Off-shore wind is not safe
        ,
        (
            Vector2D.from_bearing_and_magnitude(bearing=180, magnitude=1),
            Vector2D.from_bearing_and_magnitude(bearing=180, magnitude=1),
            EvaluationResult((False, None)),
        ),
    ],
)
def test_evaluate_wind_direction(
    wind_vector: Vector2D, coast_normal: Vector2D, evaluation_result: EvaluationResult
) -> None:
    assert (
        evaluate_wind_direction(wind_vector=wind_vector, coast_normal=coast_normal)
        == evaluation_result
    )


@pytest.mark.parametrize(
    [
        "wind_speed",
        "wind_gust",
        "min_wind_speed",
        "max_wind_speed",
        "evaluation_result",
    ],
    [
        pytest.param(
            0, 0, 10, 30, EvaluationResult((False, None)), id="wind speed too low"
        ),
        pytest.param(
            0, 40, 10, 30, EvaluationResult((False, None)), id="wind speed too high"
        ),
        pytest.param(
            20, 20, 10, 30, EvaluationResult((True, 10)), id="wind speed in range"
        ),
        pytest.param(20, 25, 10, 30, EvaluationResult((True, 7.5)), id="wind gusting"),
        pytest.param(
            20, 40, 10, 30, EvaluationResult((True, 0)), id="wind gust to score 0"
        ),
    ],
)
def test_evaluate_wind_speed(
    wind_speed: float,
    wind_gust: float,
    min_wind_speed: float,
    max_wind_speed: float,
    evaluation_result: EvaluationResult,
) -> None:
    wind_vector = Vector2D.from_bearing_and_magnitude(bearing=0, magnitude=wind_speed)
    assert (
        evaluate_wind_speed(
            wind_vector=wind_vector,
            wind_gust=wind_gust,
            min_wind_speed=min_wind_speed,
            max_wind_speed=max_wind_speed,
        )
        == evaluation_result
    )


def test_evaluate_wind_speed_with_infeasibly_small_gust_raises_error() -> None:
    wind_speed = 20
    wind_gust = 10
    wind_vector = Vector2D.from_bearing_and_magnitude(bearing=0, magnitude=wind_speed)
    with pytest.raises(ValueError, match="Wind gust cannot be less than wind speed"):
        _ = evaluate_wind_speed(
            wind_vector=wind_vector,
            wind_gust=wind_gust,
            min_wind_speed=0,
            max_wind_speed=100,
        )


# Next level up, for a point in time
def test_safe_datapoint_time_is_returned_from_all_positive_evaluations():
    score_dict = {
        "time": np.datetime64("2024-09-03T09:00Z"),
        "datapoint_scores": {
            "daylight_score": (True, None),
            "wind_direction": (True, None),
            "wind_speed": (True, None),
            "lightning": (True, None),
        },
    }
    time, is_safe = assert_if_datapoint_is_safe_overall(score_dict)
    assert is_safe
    assert time == np.datetime64("2024-09-03T09:00Z")


# Next level up, for a period of time
