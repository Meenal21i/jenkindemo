from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("SAUCE_USERNAME")
password = os.getenv("SAUCE_PASSWORD")
invalid_user = os.getenv("INVALID_USERNAME")
invalid_pass = os.getenv("INVALID_PASSWORD")

filtering_price = 20.0