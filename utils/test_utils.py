import pytest
import functools
from utils.logging import logger
from playwright.async_api import TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

def handle_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except PlaywrightTimeoutError as timeout_error:
            logger.error(f"Timeout error: {timeout_error}")
            pytest.fail("Test failed due to timeout.")
        except PlaywrightError as play_error:
            logger.error(f"Playwright error: {play_error}")
            pytest.fail("Test failed due to Playwright error.")
        except KeyboardInterrupt as keyboard_error:
            logger.error(f"Test interrupted: {keyboard_error}")
            pytest.fail("Test interrupted by user.")
        except Exception as error_message:
            logger.error(f"Unexpected error: {error_message}")
            pytest.fail("Test failed due to unexpected error.")
    return wrapper