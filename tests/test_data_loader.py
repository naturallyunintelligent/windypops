from pathlib import Path

from windy_pops.data_loader import DataLoader, Metoffice_dataloader

TEST_DATA_DIR = Path(__file__).parent / "data_for_tests"


def test_can_create_data_loader_from_file() -> None:
    test_data = TEST_DATA_DIR / "2025-sample-data.json"
    data_loader = DataLoader.from_file(test_data)
    weather_data = data_loader.data
    assert (
        weather_data["features"][0]["properties"]["location"]["name"]
        == "Shoreham-by-Sea"
    )


def test_can_create_data_loader_from_latest_cache() -> None:
    test_cache_dir = TEST_DATA_DIR  # / "test_cache"
    data_loader = DataLoader.from_latest_cache(cache_dir=test_cache_dir)
    weather_data = data_loader.data
    assert (
        weather_data["features"][0]["properties"]["location"]["name"]
        == "Shoreham-by-Sea"
    )


def test_can_create_data_loader_from_metoffice_api() -> None:
    data_loader = Metoffice_dataloader()
    assert data_loader.from_api("met_office_datahub") is not None
    weather_data = data_loader.data
    assert (
        weather_data["features"][0]["properties"]["location"]["name"]
        == "Shoreham-by-Sea"
    )
