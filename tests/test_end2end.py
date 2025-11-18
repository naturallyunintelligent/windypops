from pathlib import Path

import numpy as np

from windy_pops.constants import DATA_DIR
from windy_pops.data_loader import DataLoader
from windy_pops.windy_pops import main

TEST_DATA_DIR = Path(__file__).parent / "data"


def test_finds_one_safe_weather_window() -> None:
    safe_window = main(
        data_loader=DataLoader.from_file(DATA_DIR / Path("test_data_1.json"))
    )

    assert len(safe_window) == 1

    day, start_time, end_time = safe_window[0]
    assert day == "Tuesday"
    assert start_time == np.datetime64("2024-10-08T09:00")
    assert end_time == np.datetime64("2024-10-08T12:00")
