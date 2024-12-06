import webbrowser
from datetime import datetime
from core.constants import *

class BrowserHandler:
    def __init__(self, emulator=None):
        self.last_link_time = None
        self.emulator = emulator

    def can_open_link(self):
        if OVERLAPPING:
            return True

        current_time = datetime.now()
        if self.last_link_time is None:
            self.last_link_time = current_time
            return True

        time_diff = (current_time - self.last_link_time).total_seconds()
        if time_diff >= TIMER_SECONDS:
            self.last_link_time = current_time
            return True
        return False

    def open_url(self, url):
        if self.can_open_link():
            try:
                if USE_EMULATOR and self.emulator:
                    return self.emulator.open_url_in_emulator(url)
                else:
                    webbrowser.open(url)
                    print(f"Successfully opened URL: {url}")
                return True
            except Exception as e:
                print(f"Error opening the URL: {e}")
                return False
        else:
            print(f"Please wait {TIMER_SECONDS} seconds between opening links")
            return False