import pytest

from function.fmp_function import FMPDataError, response_frame, response_records


def test_response_records_accepts_legacy_list():
    response = [{"symbol": "AAPL", "price": 100}]

    assert response_records(response, "company profile") == response


@pytest.mark.parametrize("wrapper", ["data", "results", "result", "financials"])
def test_response_records_unwraps_new_response_shapes(wrapper):
    records = [{"symbol": "AAPL"}]

    assert response_records({wrapper: records}, "profile") == records


def test_response_frame_accepts_a_single_record():
    frame = response_frame({"symbol": "AAPL", "price": 100}, "profile")

    assert frame.to_dict("records") == [{"symbol": "AAPL", "price": 100}]


@pytest.mark.parametrize(
    "response, expected",
    [
        ({"Error Message": "Invalid API key"}, "Invalid API key"),
        ({"Information": "Legacy endpoint retired"}, "Legacy endpoint retired"),
        ({"message": "Endpoint unavailable", "status": 403}, "Endpoint unavailable"),
        ([], "No data"),
        (None, "did not return"),
    ],
)
def test_response_records_reports_api_failures(response, expected):
    with pytest.raises(FMPDataError, match=expected):
        response_records(response, "company profile")
