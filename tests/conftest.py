import pytest


@pytest.fixture
def sample_driver():
    return {"driver_name": "Test Driver", "phone_number": "9876543210"}


@pytest.fixture
def sample_collection():
    return {
        "driver_id": 1,
        "vehicle_number": "TN38AB1234",
        "collection_date": "2026-10-10",
        "morning_trips": 4,
        "evening_trips": 3,
        "morning_collection": "1200.00",
        "evening_collection": "900.00",
        "fuel_expense": "500.00",
        "other_expense": "100.00",
    }
