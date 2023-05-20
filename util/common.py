# External Libraries

import os
from urllib.parse import urljoin
import json as JSON

# Internal Libraries

# get_env(name: str, delim: str | None = None, default: str | None = None, errorOnNull: bool = False): string
# Given a variable name string, and an optional delimiter, default value, and an errorOnNull bolean
# gets the value of the given environment variable, and splits it on the delimiter if provided. If the
# variable is unset or null, and errorOnNull is set the
def get_env(name: str,
            delim: str | None = None,
            default: str | None = None,
            errorOnNull: bool = False):

    # Get the environment variable
    env: str | None = os.getenv(name)

    # Variable is none
    if env == None:
        # Error on null
        if errorOnNull:
            # Raise type error
            raise TypeError(
                f"Environment variable '{name}' is null! (Value: '{env}')")

        # Default on null
        if default:
            # Set to default
            env = default

    # Delimiter is set
    if delim != None:

        # Check for null again
        if env == None:

            # Set to empty array
            env = []

        else:  # Variable is not null

            # (Attempt to) split on delimiter
            env = env.split(delim)

    # Return variable
    return env

# ms_to_timestamp(time: int): str
# Converts a given millisecond value
# into a timestamp string
def ms_to_timestamp(time: int) -> str:
    # Get total seconds and round down
    total_seconds = time // 1000

    # Get minutes and remaining seconds
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    # Get milliseconds and pad with leading zeros
    formatted_milliseconds = str(time % 1000).zfill(3)

    # Format the time string as [M]M'SS"MMM
    timestamp = f"{minutes:01}'{seconds:02}\"{formatted_milliseconds}"

    # Return the timestamp
    return timestamp
