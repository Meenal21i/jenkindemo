import pytest
import time
import asyncio
from utils.setup_directory import create_directories, video_dirirectory, screenshot_directory
from playwright.async_api import async_playwright

@pytest.fixture(autouse=True)
def context():
    '''This is to collect the shared data between pages'''
    return {}

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    create_directories()
    yield

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def browser():
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)
    yield browser
    await browser.close()
    await p.stop()

@pytest.fixture
async def page(browser):
    page = await browser.new_page(record_video_dir=str(video_dirirectory))
    page.set_default_timeout(5000)
    yield page
    await page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = getattr(item, "page", None)
        if page:
            screenshot_path = screenshot_directory / f"{item.name}_{int(time.time())}.png"
            try:
                asyncio.run(page.screenshot(path=str(screenshot_path)))
                print(f"\nScreenshot captured: {screenshot_path}")
            except Exception as error_message:
                print(f"\nFailed to capture screenshot: {error_message}")