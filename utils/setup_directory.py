from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

screenshot_directory = BASE_DIR / "screenshots"
video_dirirectory = BASE_DIR / "videos"

def create_directories():
    screenshot_directory.mkdir(exist_ok=True)
    video_dirirectory.mkdir(exist_ok=True)