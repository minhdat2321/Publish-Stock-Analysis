import logging
import typing

import requests

from .settings import (
    INDUSTRY_VALUES,
    PERIOD_VALUES,
    SECTOR_VALUES,
    SERIES_TYPE_VALUES,
    STATISTICS_TYPE_VALUES,
    TECHNICAL_INDICATORS_TIME_DELTA_VALUES,
    TIME_DELTA_VALUES,
    BASE_URL_v3,
    BASE_URL_v4,
    BASE_URL_STABLE,
)

CONNECT_TIMEOUT = 5
READ_TIMEOUT = 30


def __return_json_stable(
    path: str, query_vars: typing.Dict
) -> typing.Optional[typing.List]:
    """Query a current FMP Stable API endpoint."""
    return _return_json(url=f"{BASE_URL_STABLE}{path.lstrip('/')}", query_vars=query_vars)


def _return_json(url: str, query_vars: typing.Dict):
    """Make an FMP request while preserving API error payloads for the caller."""
    return_var = None
    try:
        response = requests.get(
            url, params=query_vars, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
        if response.content:
            return_var = response.json()
        if not response.content or return_var == {}:
            logging.warning("Response appears to have no data. Returning empty List.")
            return_var = []
    except requests.Timeout:
        logging.error("Connection to %s timed out.", url)
    except requests.ConnectionError:
        logging.error("Connection to %s failed.", url)
    except requests.TooManyRedirects:
        logging.error("Request to %s exceeded the redirection limit.", url)
    except (requests.RequestException, ValueError) as error:
        logging.error("Request to %s failed: %s", url, error)
    return return_var

# Disable excessive DEBUG messages.
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def __return_json_v3(
    path: str, query_vars: typing.Dict
) -> typing.Optional[typing.List]:
    """
    Query URL for JSON response for v3 of FMP API.

    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :return: JSON response
    """
    url = f"{BASE_URL_v3}{path}"
    return_var = None
    try:
        response = requests.get(
            url, params=query_vars, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
        if len(response.content) > 0:
            return_var = response.json()

        if len(response.content) == 0 or (
            isinstance(return_var, dict) and len(return_var.keys()) == 0
        ):
            logging.warning("Response appears to have no data.  Returning empty List.")
            return_var = []

    except requests.Timeout:
        logging.error(f"Connection to {url} timed out.")
    except requests.ConnectionError:
        logging.error(
            f"Connection to {url} failed:  DNS failure, refused connection or some other connection related "
            f"issue."
        )
    except requests.TooManyRedirects:
        logging.error(
            f"Request to {url} exceeds the maximum number of predefined redirections."
        )
    except Exception as e:
        logging.error(
            f"A requests exception has occurred that we have not yet detailed an 'except' clause for.  "
            f"Error: {e}"
        )

    return return_var


def __return_json_v4(
    path: str, query_vars: typing.Dict
) -> typing.Optional[typing.List]:
    """
    Query URL for JSON response for v4 of FMP API.

    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :return: JSON response
    """
    url = f"{BASE_URL_v4}{path}"
    return_var = None
    try:
        response = requests.get(
            url, params=query_vars, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
        if len(response.content) > 0:
            return_var = response.json()

        if len(response.content) == 0 or (
            isinstance(return_var, dict) and len(return_var.keys()) == 0
        ):
            logging.warning("Response appears to have no data.  Returning empty List.")
            return_var = []

    except requests.Timeout:
        logging.error(f"Connection to {url} timed out.")
    except requests.ConnectionError:
        logging.error(
            f"Connection to {url} failed:  DNS failure, refused connection or some other connection related "
            f"issue."
        )
    except requests.TooManyRedirects:
        logging.error(
            f"Request to {url} exceeds the maximum number of predefined redirections."
        )
    except Exception as e:
        logging.error(
            f"A requests exception has occurred that we have not yet detailed an 'except' clause for.  "
            f"Error: {e}"
        )
    return return_var


def __validate_period(value: str) -> str:
    """
    Check to see if passed string is in the list of possible time periods.
    :param value: Period name.
    :return: Passed value or No Return
    """
    valid_values = PERIOD_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(f"Invalid period value: {value}.  Valid options: {valid_values}")


def __validate_sector(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Sectors.
    :param value: Sector name.
    :return: Passed value or No Return
    """
    valid_values = SECTOR_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(f"Invalid sector value: {value}.  Valid options: {valid_values}")


def __validate_industry(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Industries.
    :param value: Industry name.
    :return: Passed value or No Return
    """
    valid_values = INDUSTRY_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid industry value: {value}.  Valid options: {valid_values}"
        )


def __validate_time_delta(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Time Deltas.
    :param value: Time Delta name.
    :return: Passed value or No Return
    """
    valid_values = TIME_DELTA_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid time_delta value: {value}.  Valid options: {valid_values}"
        )


def __validate_series_type(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Series Type.
    :param value: Series Type name.
    :return: Passed value or No Return
    """
    valid_values = SERIES_TYPE_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid series_type value: {value}.  Valid options: {valid_values}"
        )


def __validate_statistics_type(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Statistics Type.
    :param value: Statistics Type name.
    :return: Passed value or No Return
    """
    valid_values = STATISTICS_TYPE_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid statistics_type value: {value}.  Valid options: {valid_values}"
        )


def __validate_technical_indicators_time_delta(value: str) -> str:
    """Exactly like set_time_delta() method but adds 'daily' as an option.
    :param value: Indicators Time Delta name.
    :return: Passed value or No Return
    """
    valid_values = TECHNICAL_INDICATORS_TIME_DELTA_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid time_delta value: {value}.  Valid options: {valid_values}"
        )
